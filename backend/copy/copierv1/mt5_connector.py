import MetaTrader5 as mt5
import time
import logging

logger = logging.getLogger("MT5Connector")

class MT5Connector:
    def __init__(self):
        self.current_account = None

    def connect(self, account_config):
        """
        Connects to a specific MT5 account with robust retries and delays.
        """
        login = int(account_config['login'])
        password = account_config['password']
        server = account_config['server']
        path = account_config.get('path')

        # Always shutdown previous connection to ensure clean state when switching
        if self.current_account != login or mt5.terminal_info() is None:
            if self.current_account is not None:
                mt5.shutdown()
                time.sleep(0.1) # Brief pause to allow resource release

            # Retry loop for connection
            for attempt in range(3):
                try:
                    if path:
                        if not mt5.initialize(path=path, login=login, password=password, server=server):
                            logger.warning(f"Connection attempt {attempt+1} failed for {login}: {mt5.last_error()}")
                            time.sleep(1)
                            continue
                    else:
                        if not mt5.initialize(login=login, password=password, server=server):
                            logger.warning(f"Connection attempt {attempt+1} failed for {login}: {mt5.last_error()}")
                            time.sleep(1)
                            continue
                    
                    # Verify connection success
                    info = mt5.account_info()
                    if info and info.login == login:
                        self.current_account = login
                        logger.info(f"Successfully connected to account {login}")
                        return True
                    else:
                         logger.warning(f"Initialize passed but account info mismatch/none for {login}")
                         mt5.shutdown()
                         time.sleep(0.5)

                except Exception as e:
                    logger.error(f"Exception during connection to {login}: {e}")
                    time.sleep(1)

            logger.error(f"Failed to connect to {login} after 3 attempts.")
            return False
            
        return True

    def get_account_info(self):
        return mt5.account_info()

    def shutdown(self):
        mt5.shutdown()
        self.current_account = None
