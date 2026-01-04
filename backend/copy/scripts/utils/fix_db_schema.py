import sqlite3

db_path = 'api_server/aibot.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("🔧 Iniciando reparo do banco de dados...")

# 1. Tentar adicionar a coluna se não existir
try:
    cursor.execute("ALTER TABLE users ADD COLUMN allowed_mt5_id TEXT")
    print("✅ Coluna 'allowed_mt5_id' adicionada.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("ℹ️  Coluna 'allowed_mt5_id' já existe.")
    else:
        print(f"❌ Erro ao adicionar coluna: {e}")

# 2. Atualizar o ID do cliente
try:
    print("🔄 Definindo ID do MT5 para usuário 'client'...")
    cursor.execute("UPDATE users SET allowed_mt5_id = ? WHERE username='client'", ('7409735',))
    
    # 3. Atualizar o ID do master também (só pra garantir)
    cursor.execute("UPDATE users SET allowed_mt5_id = ? WHERE username='master'", ('7409735',))
    
    conn.commit()
    print("✅ IDs atualizados com sucesso!")

    # 4. Verificar
    cursor.execute("SELECT username, role, allowed_mt5_id FROM users")
    rows = cursor.fetchall()
    print("\n📊 Estado atual da tabela Users:")
    for row in rows:
        print(row)

except Exception as e:
    print(f"❌ Erro ao atualizar dados: {e}")

conn.close()
