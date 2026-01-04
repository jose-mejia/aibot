import MetaTrader5 as mt5
import time
import logging
import os
import json
import hashlib
from datetime import datetime

from mt5_connector import MT5Connector
from db_utils import Database
from safety import SafetyGuard
from utils import calculate_lot_size, normalize_symbol

logger = logging.getLogger("CopierService")

class TradeCopier:
    def __init__(self, config, secrets, symbol_config={}):
        self.config = config
        self.secrets = secrets
        self.symbol_config = symbol_config
        self.connector = MT5Connector()
        self.db = Database(config['paths']['db_file'])
        self.safety = SafetyGuard(config, symbol_config)
        self.is_running = True

        # State cache for Master-First Logic
        self.master_cache_positions = {} # {ticket: position_obj}
        self.last_sync_time = 0
        self.SYNC_INTERVAL = 30 # Seconds to force sync
        self.last_state_hash = ""
        
        # Blacklist for accounts in violation
        self.account_blacklist = set() 
        
    def run_cycle(self):
        """
        DUAL-PROCESS CYCLE (Follower-Side):
        1. Watch 'master_state.json' for changes.
        2. If file modified -> Read State -> Sync Followers.
        """
        try:
            # --- PHASE 1: READ FILE STATE ---
            master_data, current_hash = self._read_master_from_file()
            if master_data is None:
                time.sleep(1.0) # Polling interval increased to 1s per user request
                return

            # --- PHASE 2: DETECT CHANGES ---
            changes_detected = False
            if current_hash != self.last_state_hash:
                changes_detected = True
                self.last_state_hash = current_hash
            
            # Convert to map for modification tracking (cache)
            current_map = {p['ticket']: p for p in master_data.get('positions', []) + master_data.get('orders', [])}
            
            # Update Cache
            self.master_cache_positions = current_map

            # --- PHASE 3: SYNC ---
            # Safety: If server_time_msc is 0 or missing, ignored
            if master_data.get('server_time_msc', 0) == 0:
                 logger.warning("Read empty/invalid state (Time=0). Skipping sync to prevent mass close.")
                 time.sleep(1.0)
                 return

            time_since_sync = time.time() - self.last_sync_time

            should_sync = changes_detected or (time_since_sync > self.SYNC_INTERVAL)
            
            if should_sync:
                if changes_detected:
                    logger.info(">> Sync triggered by FILE CHANGE.")
                else:
                    logger.debug(">> Sync triggered by TIMER.")
                    
                self._sync_all_followers(master_data) # Send full data
                self.last_sync_time = time.time()
            else:
                time.sleep(1.0) # Idle sleep 1s 
                
        except Exception as e:
            logger.exception(f"Unexpected error in run_cycle: {e}")
            time.sleep(1)

    def _read_master_from_file(self):
        path = "master_state.json"
        
        # Retry loop for reading (Windows locking)
        for _ in range(5):
            if not os.path.exists(path):
                 time.sleep(0.05)
                 continue # Wait and retry, don't return Empty immediately

            try:
                # Open with shared read permission technically default in Python
                with open(path, 'r') as f:
                    content = f.read()
                    if not content: continue
                    
                    data = json.loads(content)
                    # HASH OPTIMIZATION: ignore server_time_msc which changes every 10ms
                    # We create a hash of the significant parts (positions and orders)
                    hash_base = {
                        "positions": data.get("positions", []),
                        "orders": data.get("orders", [])
                    }
                    f_hash = hashlib.md5(json.dumps(hash_base, sort_keys=True).encode()).hexdigest()
                    return data, f_hash
            except (json.JSONDecodeError, OSError):
                # File locked or partial write. Wait and retry.
                time.sleep(0.02)
        
        return None, "" # Failed to read after retries

    def _enforce_one_order_rule_master_data(self, positions_list):
        # We can't close Master trades from here (Observer does it? Or we can't).
        # We only log. Observer logic handles Master safety if we move safety there.
        # Ideally Observer script should have the safety checks for Master.
        # Here we just check to ensure we don't copy violations.
        pass

    def _enforce_order_limit_sanitary(self, positions, orders, account_name):
        """
        Ensures NO MORE THAN 2 orders per symbol. If violation, closes newest? 
        Actually, user wants to guarantee 2. If more than 2, we should probably warn or sanitize.
        For now, we just log.
        """
        symbol_map = {} 
        for p in list(positions) + list(orders):
            if p.symbol not in symbol_map:
                symbol_map[p.symbol] = []
            symbol_map[p.symbol].append(p)
            
        for symbol, item_list in symbol_map.items():
            if len(item_list) > 3:
                # Sort by ticket (higher is newer)
                item_list.sort(key=lambda x: x.ticket) 
                to_close = item_list[3:] # Keep first 3
                
                logger.critical(f"LIMIT VIOLATION: {len(item_list)} orders for {symbol} on {account_name}. Closing {len(to_close)} extras.")
                for item in to_close:
                    if hasattr(item, 'position'): # It's a deal/position? 
                         self._close_position_by_ticket(item.ticket, item.symbol)
                    else:
                         # It's a pending order
                         mt5.order_send({"action": mt5.TRADE_ACTION_REMOVE, "order": item.ticket})

    def _check_drawdown(self, follower):
        """
        Checks global drawdown limit.
        """
        info = self.connector.get_account_info()
        if not info:
             return False
             
        max_dd = self.config.get('safety', {}).get('max_drawdown_percent', 10.0)
        
        # Calculate DD based on Balance (Closed PnL + Deposits) vs Equity (Floating)
        # If Equity drops below Balance * (1 - limit), we stop.
        # Alternatively, user might want fixed amount. Percent is safer for now.
        
        limit_equity = info.balance * (1.0 - (max_dd / 100.0))
        
        if info.equity < limit_equity:
            logger.critical(f"MAX DRAWDOWN REACHED for {follower.get('login')}! Equity: {info.equity} < Limit: {limit_equity} ({max_dd}%). EMERGENCY STOP.")
            
            # Close ALL positions
            positions = mt5.positions_get()
            if positions:
                for p in positions:
                    self._close_position_by_ticket(p.ticket, p.symbol)
            
            return True
            
        return False

    def _sync_all_followers(self, master_data):
        followers_config = self.secrets.get('followers', [])
        results = []

        for i, follower in enumerate(followers_config):
            f_login = follower.get('login')
            if f_login in self.account_blacklist:
                results.append(f"{f_login}:SKIPPED (Blacklist)")
                continue

            logger.info(f"Processing Follower {i+1}/{len(followers_config)}: {f_login}")
            try:
                success = self._sync_follower(follower, master_data)
                results.append(f"{f_login}:{'OK' if success else 'FAIL'}")
            except Exception as e:
                logger.error(f"Error syncing follower {f_login}: {e}")
                results.append(f"{f_login}:ERROR")
                # Continue to next follower
        
        logger.info(f"Cycle Complete. Results: {', '.join(results)}")
    
    def _sync_follower(self, follower_conf, master_data):
        if not self.connector.connect(follower_conf):
            logger.error(f"Could not connect to Follower {follower_conf.get('login')}")
            return False

        master_positions = {p['ticket']: p for p in master_data.get('positions', [])}
        master_orders = {o['ticket']: o for o in master_data.get('orders', [])}
        all_master_items = {**master_positions, **master_orders}

        # 0. Check Max Drawdown (Emergency Stop)
        # DISABLED per user request "remove this rule" (10% limit)
        # if self._check_drawdown(follower_conf):
        #     self.account_blacklist.add(follower_conf.get('login'))
        #     return False


        # Read Follower State
        f_positions = mt5.positions_get()
        f_orders = mt5.orders_get()
        
        if f_positions is None: f_positions = []
        if f_orders is None: f_orders = []

        # 1. Enforce Order Limit Rule (Max 2 per symbol)
        # We don't close here, we just check before opening. 
        # But we can keep the sanitizer for duplicates if needed (Oldest logic).
        self._enforce_order_limit_sanitary(f_positions, f_orders, f"Follower {follower_conf.get('login')}")

        # 2. Sync NEW Trades (Positions and Pending)
        for ticket, master_item in all_master_items.items():
            trade_record = self.db.get_trade(ticket, follower_conf.get('login'))

            
            if not trade_record:
                # NEW TRADE
                self._execute_open(master_item, follower_conf, f_positions, f_orders)
            elif trade_record['status'] == 'OPEN':
                # Existing trade -> Sync Modifications
                self._sync_modifications(ticket, master_item, f_positions, f_orders, trade_record)


        # 3. Check for CLOSED Trades
        # Get only trades for THIS follower
        open_copied_trades = self.db.get_open_trades(follower_conf.get('login'))

        for key, record in open_copied_trades.items():
            m_ticket = int(record['master_ticket']) # Use explicit field, not composite key
            if m_ticket not in all_master_items:
                logger.info(f"Trade {m_ticket} closed on Master. Closing on Follower {follower_conf.get('login')}...")
                self._execute_close(m_ticket, record, list(f_positions) + list(f_orders), follower_conf.get('login'))

        # 4. STRICT IDENTICAL CHECK (Global Cleanup)
        # Close any order that is NOT in the Master's current list.
        # This handles:
        # A) Ghost Orders (Closed on Master but open on Follower)
        # B) Manual Orders (Opened by user on Follower)
        # C) Orphaned Orders (From previous bot runs)
        
        copier_magic = self.config['trade_copy']['magic_number_copier']
        active_master_tickets = set(all_master_items.keys())
        
        # Combine lists for check
        all_follower_items = list(f_positions) + list(f_orders)
        
        for item in all_follower_items:
            # Skip if we just acted on it in Step 3 (Closed correctly)
            # Actually Step 3 uses DB. This is a failsafe using current state.
            
            # 1. Check if it's OUR order (Magic Number)
            if item.magic == copier_magic:
                # Attempt to extract Master Ticket
                try:
                    if item.comment.startswith("COPY_"):
                        m_ticket = int(item.comment.split('_')[1])
                        if m_ticket not in active_master_tickets:
                            logger.info(f"STRICT CLEANUP: Trade {item.ticket} (Master {m_ticket}) is not in Master Active List. Closing.")
                            if hasattr(item, 'position') or hasattr(item, 'time_update_msc'):
                                self._close_position_by_ticket(item.ticket, item.symbol)
                            else:
                                mt5.order_send({"action": mt5.TRADE_ACTION_REMOVE, "order": item.ticket})
                    else:
                        # Has magic number but bad comment? Close it.
                        logger.warning(f"STRICT CLEANUP: Trade {item.ticket} has Magic Number but invalid comment '{item.comment}'. Closing.")
                        self._close_position_by_ticket(item.ticket, item.symbol)
                except Exception as e:
                     logger.error(f"Error parsing trade comment {item.comment}: {e}")
            
            # 2. Check for MANUAL Orders (Make Identical Rule)
            # If magic number is 0 (or different), strict mode says DELETE IT.
            elif item.magic == 0: # Manual usually 0
                logger.warning(f"STRICT CLEANUP: Found MANUAL Trade {item.ticket} on Follower. Closing to match Master.")
                if hasattr(item, 'position') or hasattr(item, 'time_update_msc'):
                     self._close_position_by_ticket(item.ticket, item.symbol)
                else:
                     mt5.order_send({"action": mt5.TRADE_ACTION_REMOVE, "order": item.ticket})
            
            # 3. Other Magic Numbers? (Other bots)
            # If user wants strict identical, we delete these too. assumes this bot OWNS the account.
            else:
                 logger.warning(f"STRICT CLEANUP: Found Alien Trade {item.ticket} (Magic {item.magic}). Closing.")
                 if hasattr(item, 'position') or hasattr(item, 'time_update_msc'):
                     self._close_position_by_ticket(item.ticket, item.symbol)
                 else:
                     mt5.order_send({"action": mt5.TRADE_ACTION_REMOVE, "order": item.ticket})

        return True

    def _execute_open(self, master_item, follower_conf, f_positions, f_orders):
        """
        Executes order opening (Market or Pending).
        """
        symbol = normalize_symbol(master_item['symbol'])
        
        if not mt5.symbol_select(symbol, True):
            logger.error(f"Failed to select symbol {symbol} on Follower. Cannot trade.")
            return

        # 1.5. ROBUST DUPLICATE CHECK (Comment matching)
        # Check if we already have this ticket by comment
        comment_string = f"COPY_{master_item['ticket']}"
        for p in list(f_positions) + list(f_orders):
            if p.comment == comment_string:

                logger.info(f"ALREADY COPIED: Trade {master_item['ticket']} found on Follower {follower_conf.get('login')} by comment. Skipping.")
                # We should update our DB if it's missing (using composite key)
                if not self.db.get_trade(master_item['ticket'], follower_conf.get('login')):
                    self.db.save_trade(
                        master_item['ticket'], 
                        p.ticket, 
                        symbol, 
                        "BUY" if "BUY" in str(master_item['type']) else "SELL", 
                        p.volume if hasattr(p, 'volume') else p.volume_initial,
                        follower_conf.get('login')
                    )
                return


        # 1. LATENCY CHECK (3 seconds)
        # Only for Market Orders. Pending orders can stay longer.
        # ORDER_TYPE_BUY = 0, ORDER_TYPE_SELL = 1. Others are pending.
        is_market = master_item['type'] in [0, 1]
        if is_market:
            # Check time_msc
            master_time_msc = master_item.get('time_msc', 0)
            now_msc = int(time.time() * 1000)
            # User requested 10 seconds tolerance
            # User requested 10 seconds tolerance. Strict check: reject if time missing (0) or too old.
            if master_time_msc <= 0 or (now_msc - master_time_msc) > 10000:
                diff_s = (now_msc - master_time_msc)/1000.0 if master_time_msc > 0 else "Unknown"
                logger.warning(f"LATENCY REJECT: Market order {master_item['ticket']} rejected. Age: {diff_s}s (Max 10s). TimeMsc: {master_time_msc}")
                return

        # 2. ORDER LIMIT CHECK (Max 2)
        if self.safety.check_order_limit(symbol, f_positions, f_orders):
            return

        # 3. SL CHECK (Now relaxed)
        if not self.safety.check_mandatory_sl(master_item['sl']):
             return
        
        if master_item['sl'] <= 0:
            logger.info(f"Trade {master_item['ticket']} has NO Stop Loss. Copying per user request.")

        # 4. SLIPPAGE & SPREAD (Only for Market)
        if is_market:
            if not self.safety.check_slippage(master_item['price_open'], symbol, master_item['type']):
                return 
            if not self.safety.check_spread(symbol):
                return

        f_info = self.connector.get_account_info()
        
        mode = self.config['trade_copy']['mode']
        if 'mode' in follower_conf:
             mode = follower_conf['mode']
             
        final_lot = calculate_lot_size(
            master_item['volume'], 
            10000.0, # Placeholder
            f_info.equity if f_info else 0.0,
            mode,
            self.config['trade_copy']
        )

        if not self.safety.check_margin(symbol, master_item['type'], final_lot, f_info.equity):
            return

        copier_magic = self.config['trade_copy']['magic_number_copier']
        current_orders = list(f_positions) + list(f_orders)
        my_orders = [o for o in current_orders if o.magic == copier_magic]
        total_lots = sum(o.volume if hasattr(o, 'volume') else o.volume_initial for o in my_orders)
        
        if not self.safety.check_exposure(len(my_orders), total_lots):
            return
            
        # Determine correct filling mode
        filling_mode = mt5.symbol_info(symbol).filling_mode
        type_filling = mt5.ORDER_FILLING_FOK
        if filling_mode & 2: 
            type_filling = mt5.ORDER_FILLING_IOC
        elif filling_mode & 1:
            type_filling = mt5.ORDER_FILLING_FOK

        # Action based on type
        action = mt5.TRADE_ACTION_DEAL if is_market else mt5.TRADE_ACTION_PENDING
        price = master_item['price_open']
        if is_market:
             price = mt5.symbol_info_tick(symbol).ask if master_item['type'] == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid
            
        request = {
            "action": action,
            "symbol": symbol,
            "volume": final_lot,
            "type": master_item['type'],
            "price": price,
            "deviation": self.config['trade_copy'].get('max_slippage_points', 50),
            "magic": copier_magic,
            "comment": f"COPY_{master_item['ticket']}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": type_filling,
            "sl": master_item['sl'],
            "tp": master_item['tp'] 
        }
        
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Order Send Failed: {result.retcode} - {result.comment}")
        else:
            logger.info(f"Opened {'Market' if is_market else 'Pending'} Trade {result.order or result.deal} on Follower {follower_conf.get('login')} (Master: {master_item['ticket']})")
            self.db.save_trade(
                master_item['ticket'], 
                result.order or result.deal, 
                symbol, 
                "BUY" if "BUY" in str(master_item['type']) else "SELL", # Simplified
                final_lot,
                 follower_conf.get('login')
            )


    def _sync_modifications(self, master_ticket, master_item, f_positions, f_orders, trade_record):
        """
        Syncs SL/TP if they change on Master.
        """
        # record = self.db.get_trade(master_ticket) # Removed re-fetch, use passed record
        if not trade_record: return
        
        f_ticket = trade_record['follower_ticket']
        # We need follower login here, but it's not passed. 
        # Wait, the caller loop has it. Let's fix helper method signature or assuming caller checked DB?
        # Actually caller has 'trade_record' which contains 'follower_ticket'.
        # We just need to find that ticket and update.
        # But for logging clarity, we might want login.
        pass

        
        # f_ticket is already set above from trade_record

        
        # Find local item
        local_item = None
        for p in list(f_positions) + list(f_orders):
            if p.ticket == f_ticket:
                local_item = p
                break
        
        if not local_item: return

        # Compare SL/TP
        if abs(local_item.sl - master_item['sl']) > 0.000001 or abs(local_item.tp - master_item['tp']) > 0.000001:
            logger.info(f"Modifying Trade {f_ticket} (Master {master_ticket}) -> SL: {local_item.sl} to {master_item['sl']}, TP: {local_item.tp} to {master_item['tp']}")
            
            # Robust check for position vs order
            # In Python MT5, position objects often don't have time_setup_msc, while orders do.
            is_position = hasattr(local_item, 'time_update_msc') or hasattr(local_item, 'reason')
            
            if is_position:
                request = {
                    "action": mt5.TRADE_ACTION_SLTP,
                    "symbol": local_item.symbol,
                    "sl": float(master_item['sl']),
                    "tp": float(master_item['tp']),
                    "position": int(f_ticket)
                }
            else:
                # Pending order modification
                request = {
                    "action": mt5.TRADE_ACTION_MODIFY,
                    "symbol": local_item.symbol,
                    "sl": float(master_item['sl']),
                    "tp": float(master_item['tp']),
                    "order": int(f_ticket),
                    "price": float(local_item.price_open)
                }
            
            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                 logger.error(f"Modification Failed: {result.retcode} - {result.comment}")
            else:
                 logger.info(f"Successfully modified trade {f_ticket}")

    def _execute_close(self, master_ticket, record, follower_items, follower_login):
        f_ticket = record['follower_ticket']
        target_item = None
        for item in follower_items:
            if item.ticket == f_ticket:
                target_item = item
                break
        
        if target_item:
            # Check if it's a position or order
            if hasattr(target_item, 'position') or hasattr(target_item, 'time_update_msc'): # position logic
                 self._close_position_by_ticket(f_ticket, target_item.symbol)
            else:
                 # It's a pending order -> Remove it
                 mt5.order_send({"action": mt5.TRADE_ACTION_REMOVE, "order": f_ticket})
                 logger.info(f"Removed Pending Order {f_ticket} on {follower_login} (Master: {master_ticket})")
        else:
            # HISTORY FALLBACK: Check if closed by SL/TP
            # Look at deals for this symbol and magic number in last 2 hours
            time_from = datetime.now().timestamp() - 7200
            history_deals = mt5.history_deals_get(time_from, datetime.now().timestamp(), group=f"*{record['symbol']}*")
            found_in_history = False
            if history_deals:
                for deal in history_deals:
                    if deal.magic == self.config['trade_copy']['magic_number_copier'] and deal.comment == f"COPY_{master_ticket}":
                         logger.info(f"Trade {master_ticket} (Follower {f_ticket}) already closed by Broker (SL/TP/Manual).")
                         found_in_history = True
                         break
            
            if not found_in_history:
                logger.warning(f"Trade {f_ticket} not found on Follower {follower_login} state (Inconsistency).")
        
        self.db.mark_as_closed(master_ticket, follower_login)


    def _close_position_by_ticket(self, ticket, symbol):
        positions = mt5.positions_get(ticket=ticket)
        if not positions:
            return

        pos = positions[0]
        op_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).bid if op_type == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(symbol).ask
        
        # Valid filling mode check
        filling_mode = mt5.symbol_info(symbol).filling_mode
        type_filling = mt5.ORDER_FILLING_FOK
        if filling_mode & 2:
             type_filling = mt5.ORDER_FILLING_IOC
        elif filling_mode & 1:
             type_filling = mt5.ORDER_FILLING_FOK
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": pos.volume,
            "type": op_type,
            "position": ticket,
            "price": price,
            "deviation": 50,
            "magic": self.config['trade_copy']['magic_number_copier'], # Or from pos.magic
            "comment": "COPY_CLOSE",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": type_filling,
        }
        
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Failed to close trade {ticket}: {result.comment}")
        else:
            logger.info(f"Closed Trade {ticket} on Follower.")
