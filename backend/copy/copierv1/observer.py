import MetaTrader5 as mt5
import json
import time
import os
import logging
import sys
from datetime import datetime

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - OBSERVER - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("Observer")

STATE_FILE = "master_state.json"

def load_json(path):
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {}

import random

def save_state(positions, orders):
    """
    Saves the list of positions and pending orders to JSON file.
    """
    pos_data = []
    for p in positions:
        pos_data.append({
            "ticket": p.ticket,
            "symbol": p.symbol,
            "type": p.type,
            "volume": p.volume,
            "price_open": p.price_open,
            "sl": p.sl,
            "tp": p.tp,
            "time": p.time,
            "time_msc": p.time_msc,
            "magic": p.magic,
            "state": "POSITION"
        })
    
    ord_data = []
    for o in orders:
        ord_data.append({
            "ticket": o.ticket,
            "symbol": o.symbol,
            "type": o.type,
            "volume": o.volume_initial,
            "price_open": o.price_open,
            "sl": o.sl,
            "tp": o.tp,
            "time": o.time_setup,
            "time_msc": o.time_setup_msc,
            "magic": o.magic,
            "state": "ORDER" # Pending order
        })

    data = {
        "positions": pos_data,
        "orders": ord_data,
        "server_time_msc": int(time.time() * 1000)
    }
    
    # Atomic write pattern to prevent reading half-written file
    temp_file = f"{STATE_FILE}.tmp"
    try:
        with open(temp_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        # Retry rename (Windows file lock fix)
        # We try for up to 1 second
        max_retries = 50
        for i in range(max_retries):
            try:
                if os.path.exists(STATE_FILE):
                    os.replace(temp_file, STATE_FILE)
                else:
                    os.rename(temp_file, STATE_FILE)
                break
            except OSError:
                # Collision. Wait random time (1-10ms)
                time.sleep(random.randint(1, 10) / 1000.0) 
    except Exception:
        pass # If we fail after all retries, just skip this tick. No need to spam logs.
    
    # Cleanup if needed
    if os.path.exists(temp_file):
        try:
            os.remove(temp_file)
        except:
             pass

def main():
    # Load Accounts
    try:
        with open('accounts.json', 'r') as f:
            accounts = json.load(f)
            master_conf = accounts['master']
    except Exception as e:
        logger.critical(f"Failed to load accounts.json: {e}")
        return

    # Connect to Master
    logger.info(f"Connecting to Master {master_conf.get('login')}...")
    if not mt5.initialize(
        path=master_conf.get('path'),
        login=master_conf.get('login'),
        password=master_conf.get('password'),
        server=master_conf.get('server')
    ):
        logger.critical(f"Failed to connect to Master: {mt5.last_error()}")
        return

    logger.info("Connected. Monitoring positions...")
    
    last_count = -1
    
    try:
        while True:
            positions = mt5.positions_get()
            orders = mt5.orders_get()
            
            if positions is None:
                logger.error("Failed to get positions")
                time.sleep(1)
                continue
            
            if orders is None:
                logger.error("Failed to get pending orders")
                orders = []
                
            # Log changes logic
            total_active = len(positions) + len(orders)
            if total_active != last_count:
                logger.info(f"State Change: {len(positions)} positions, {len(orders)} pending orders.")
                last_count = total_active
            
            save_state(positions, orders)
            
            # Fast poll
            time.sleep(0.01) 
            
    except KeyboardInterrupt:
        logger.info("Stopping Observer...")
    finally:
        mt5.shutdown()

if __name__ == "__main__":
    main()
