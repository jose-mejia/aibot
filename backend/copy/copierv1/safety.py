import MetaTrader5 as mt5
import logging

logger = logging.getLogger("SafetyGuard")

class SafetyGuard:
    def __init__(self, config, symbol_config={}):
        self.config = config
        self.symbol_config = symbol_config

    def check_slippage(self, master_price, follower_symbol, order_type):
        """
        Checks if the current price on follower deviates too much from master's entry price.
        """
        # Default global
        max_slippage = self.config['trade_copy'].get('max_slippage_points', 50)
        
        # Check for override
        # We try to match exact symbol or check if symbol config key is part of the symbol name (e.g. BTCUSD matching BTCUSD.m)
        for sym_key, settings in self.symbol_config.items():
            if sym_key in follower_symbol:
                val = settings.get('max_slippage_points')
                if val:
                    max_slippage = val
                    logger.debug(f"Using override slippage for {follower_symbol}: {max_slippage}")
                break

        tick = mt5.symbol_info_tick(follower_symbol)
        
        if tick is None:
            logger.error(f"Failed to get tick for {follower_symbol}")
            return False

        current_price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid
        point = mt5.symbol_info(follower_symbol).point
        
        diff_points = abs(master_price - current_price) / point
        
        if diff_points > max_slippage:
            logger.warning(f"Slippage too high! Master: {master_price}, Follower: {current_price}, Diff: {diff_points} pts (Max: {max_slippage})")
            return False
            
        return True

    def check_spread(self, symbol):
        """
        Checks if current spread is within acceptable limits.
        """
        max_spread = self.config['trade_copy'].get('max_spread_points', 20)
        
        # Check for override
        for sym_key, settings in self.symbol_config.items():
            if sym_key in symbol:
                val = settings.get('max_spread_points')
                if val:
                    max_spread = val
                    logger.debug(f"Using override spread for {symbol}: {max_spread}")
                break
                
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return False
            
        point = mt5.symbol_info(symbol).point
        spread_points = (tick.ask - tick.bid) / point
        
        if spread_points > max_spread:
            logger.warning(f"Spread too high for {symbol}: {spread_points} pts (Max: {max_spread})")
            return False
        
        return True

    def check_margin(self, symbol, order_type, volume, account_equity):
        """
        Checks if there is enough free margin for the trade.
        """
        # For simplicity in this MVP, we use a basic check. 
        # MT5's order_calc_margin can be used but requires connection context.
        # Here we rely on account Info from caller if possible, or just skip if complex.
        # Assuming the caller has checked connectivity.
        
        try:
            margin_required = mt5.order_calc_margin(order_type, symbol, volume, mt5.symbol_info_tick(symbol).ask)
            account_info = mt5.account_info()
            
            if account_info and account_info.margin_free < margin_required:
                logger.error(f"Insufficient Margin! Required: {margin_required}, Free: {account_info.margin_free}")
                return False
        except Exception as e:
            logger.error(f"Margin check failed with exception: {e}")
            # Fail safe: if we can't calculate, we don't trade? 
            # Or we allow and let the server reject. 
            # Risk-averse: return False.
            return False

        return True

    def check_exposure(self, order_count, total_lots):
        """
        Checks if the account has exceeded max trades or max lot exposure.
        """
        max_trades = self.config['trade_copy'].get('max_exposure_trades', 5)
        max_lots = self.config['trade_copy'].get('max_exposure_lots', 10.0)
        
        # Global trade count limit REMOVED per user request (was limiting total trades across all symbols).
        # We now rely only on check_order_limit (per symbol) and max_lots (global risk).
        # if order_count >= max_trades:
        #    logger.warning(f"Max trades limit reached ({order_count}/{max_trades}). Rejecting new order.")
        #    return False

            
        if total_lots >= max_lots:
            logger.warning(f"Max lot exposure reached ({total_lots}/{max_lots}). Rejecting new order.")
            return False
            
        return True

    def check_order_limit(self, symbol, positions, orders=[]):
        """
        Ensures there are at most 2 orders (positions or pending) for this symbol.
        Returns False if valid (<= 2 orders).
        Returns True if violation (> 2 orders).
        """
        count = 0
        for p in positions:
            if p.symbol == symbol:
                count += 1
        for o in orders:
            if o.symbol == symbol:
                count += 1
        
        if count >= 3:
            logger.warning(f"LIMIT REACHED: {count} orders already exist for {symbol}. Max is 3.")
            return True
        return False

    def check_mandatory_sl(self, master_sl):
        """
        User now allows copying without SL. We log a warning but return True.
        """
        if master_sl is None or master_sl <= 0:
            logger.warning("Master Order has NO Stop Loss. Copying anyway per user request.")
            return True
        return True
