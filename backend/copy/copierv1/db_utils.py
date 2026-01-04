import json
import os
import threading
from datetime import datetime

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.lock = threading.Lock()
        self._ensure_db()

    def _ensure_db(self):
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump({}, f)

    def load_data(self):
        with self.lock:
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}

    def save_trade(self, master_ticket, follower_ticket, symbol, action, volume, follower_login):
        data = self.load_data()
        key = f"{master_ticket}_{follower_login}"
        data[key] = {
            "master_ticket": master_ticket,
            "follower_ticket": follower_ticket,
            "follower_login": follower_login,
            "symbol": symbol,
            "action": action,
            "volume": volume,
            "status": "OPEN",
            "timestamp": datetime.now().isoformat()
        }
        with self.lock:
            with open(self.db_file, 'w') as f:
                json.dump(data, f, indent=4)

    def mark_as_closed(self, master_ticket, follower_login):
        data = self.load_data()
        key = f"{master_ticket}_{follower_login}"
        if key in data:
            data[key]["status"] = "CLOSED"
            data[key]["closed_at"] = datetime.now().isoformat()
            with self.lock:
                with open(self.db_file, 'w') as f:
                    json.dump(data, f, indent=4)
    
    def get_trade(self, master_ticket, follower_login):
        data = self.load_data()
        key = f"{master_ticket}_{follower_login}"
        return data.get(key)

    def get_open_trades(self, follower_login=None):
        """Returns all trades that are marked as OPEN, optionally filtered by follower"""
        data = self.load_data()
        if follower_login:
            return {k: v for k, v in data.items() if v.get("status") == "OPEN" and str(v.get("follower_login")) == str(follower_login)}
        return {k: v for k, v in data.items() if v.get("status") == "OPEN"}
