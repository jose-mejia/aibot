import sqlite3
import os

DB_PATH = os.path.join("api_server", "aibot.db")

def check_users():
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print(f"\n📂 Checking Database: {DB_PATH}")
        print("-" * 60)
        
        # Check columns in users table
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"Structure: {columns}")
        
        if 'mt5_path' not in columns:
            print("❌ CRITICAL: 'mt5_path' column is MISSING!")
        else:
            print("✅ Column 'mt5_path' exists.")

        print("-" * 60)
        print(f"{'ID':<4} | {'Username':<15} | {'Role':<10} | {'MT5 ID':<15} | {'MT5 Path'}")
        print("-" * 60)

        cursor.execute("SELECT id, username, role, allowed_mt5_id, mt5_path FROM users")
        rows = cursor.fetchall()
        
        for row in rows:
            uid, user, role, mt5id, path = row
            # Handle None
            mt5id = mt5id if mt5id else "NONE"
            path = path if path else "NONE"
            print(f"{uid:<4} | {user:<15} | {role:<10} | {mt5id:<15} | {path}")

        print("-" * 60)
        conn.close()

    except Exception as e:
        print(f"❌ SQL Error: {e}")

if __name__ == "__main__":
    check_users()
