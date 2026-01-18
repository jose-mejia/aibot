
import sqlite3
import os

try:
    db_path = r'api_server/aibot.db'
    if not os.path.exists(db_path):
        print(f"DB not found at {db_path}")
        exit(1)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT mt5_path, allowed_mt5_id FROM users WHERE role='MASTER'")
    row = cursor.fetchone()
    
    if row:
        print(f"FOUND_PATH: {row[0]}")
        print(f"FOUND_ID: {row[1]}")
    else:
        print("No MASTER user found")
        
    conn.close()
except Exception as e:
    print(f"Error: {e}")
