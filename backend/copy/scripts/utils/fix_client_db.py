import sqlite3

db_path = 'api_server/aibot.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Checar usuário client
try:
    cursor.execute("SELECT username, role, allowed_mt5_id FROM users WHERE username='client'")
    row = cursor.fetchone()
    print(f"👤 Usuário Client no DB: {row}")

    # 2. Atualizar allowed_mt5_id para 7409735
    if row:
        print("🔄 Atualizando allowed_mt5_id para 7409735...")
        cursor.execute("UPDATE users SET allowed_mt5_id = ? WHERE username='client'", ('7409735',))
        conn.commit()
        print("✅ Atualizado com sucesso!")
        
        # Verificar novamente
        cursor.execute("SELECT username, role, allowed_mt5_id FROM users WHERE username='client'")
        row_new = cursor.fetchone()
        print(f"👤 Novo estado: {row_new}")
    else:
        print("❌ Usuário 'client' não encontrado!")

except Exception as e:
    print(f"❌ Erro: {e}")

conn.close()
