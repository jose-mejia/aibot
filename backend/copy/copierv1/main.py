import json
import logging
import time
import os
import sys
from V1.copier_service import TradeCopier

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("copier.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("Main")

def load_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load {path}: {e}")
        return None

def main():
    logger.info("Starting Trade Copier MVP...")

    # Load Configs
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    accounts_path = os.path.join(os.path.dirname(__file__), 'accounts.json')
    symbols_path = os.path.join(os.path.dirname(__file__), 'symbols.json')
    
    config = load_json(config_path)
    accounts = load_json(accounts_path)
    symbols = load_json(symbols_path) or {}
    
    if not config or not accounts:
        logger.critical("Missing configuration files. Exiting.")
        return

    # Check for credentials
    if accounts['master']['password'] == "MASTER_PASSWORD_HERE":
        logger.warning("!!! WARNING: Default credentials detected in accounts.json. Please update them. !!!")

    copier = TradeCopier(config, accounts, symbols)

    logger.info("Copier Service Initialized. Entering Main Loop (Press Ctrl+C to Stop).")

    try:
        while True:
            start_time = time.time()
            
            copier.run_cycle()
            
            # Tick Interval logic
            elapsed = time.time() - start_time
            sleep_time = (config['system']['tick_interval_ms'] / 1000.0) - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
            
            # Cooldown enforcement
            if sleep_time < 0.1:
                time.sleep(0.1) # Minimum safety sleep

    except KeyboardInterrupt:
        logger.info("Shutdown signal received. Exiting.")
        copier.connector.shutdown()
    except Exception as e:
        logger.critical(f"Critical Failure: {e}")
        copier.connector.shutdown()
        raise

if __name__ == "__main__":
    main()
