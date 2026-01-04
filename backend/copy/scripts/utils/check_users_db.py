import sqlite3
import os

files = [r"c:\Users\josemejia\dev\python\aibot\backend\copy\api_server\aibot.db", 
         r"c:\Users\josemejia\dev\python\aibot\backend\copy\api_server\copier.db"]

for db_path in files:
    if not os.path.exists(db_path):
        continue
    print(f"\n--- Verificando: {os.path.basename(db_path)} ---")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tabelas encontradas: {[t[0] for t in tables]}")
        
        if ('users',) in tables:
            cursor.execute("SELECT id, username, allowed_mt5_id FROM users")
            users = cursor.fetchall()
            for user in users:
                print(f"ID: {user[0]} | Username: {user[1]} | MT5 ID: {user[2]}")
        conn.close()
    except Exception as e:
        print(f"Erro ao ler {db_path}: {e}")
