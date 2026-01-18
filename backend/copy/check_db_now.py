import sqlite3
import os

db_path = os.path.join("api_server", "aibot.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\n" + "="*100)
print("BANCO DE DADOS: api_server/aibot.db")
print("="*100)

cursor.execute("SELECT id, username, allowed_mt5_id, mt5_path FROM users")
rows = cursor.fetchall()

print(f"\n{'ID':<5} | {'Username':<15} | {'MT5 ID':<15} | {'MT5 Path'}")
print("-" * 100)

for row in rows:
    id_val, username, mt5_id, mt5_path = row
    mt5_id_str = str(mt5_id) if mt5_id else "NULL"
    mt5_path_str = mt5_path if mt5_path else "NULL"
    print(f"{id_val:<5} | {username:<15} | {mt5_id_str:<15} | {mt5_path_str}")

print("="*100 + "\n")

conn.close()
