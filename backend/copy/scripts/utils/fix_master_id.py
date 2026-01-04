import sqlite3

db_path = 'api_server/aibot.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("🔧 Corrigindo ID do Master no Banco de Dados...")

try:
    # Definir ID correto para o Master
    master_id = '11629107'
    cursor.execute("UPDATE users SET allowed_mt5_id = ? WHERE username='master'", (master_id,))
    
    # Garantir que o Client continue certo (7409735)
    client_id = '7409735'
    cursor.execute("UPDATE users SET allowed_mt5_id = ? WHERE username='client'", (client_id,))
    
    conn.commit()
    print("✅ IDs atualizados com sucesso!")

    # Verificar
    cursor.execute("SELECT username, role, allowed_mt5_id FROM users")
    rows = cursor.fetchall()
    print("\n📊 Estado atual da tabela Users:")
    for row in rows:
        print(row)

except Exception as e:
    print(f"❌ Erro ao atualizar dados: {e}")

conn.close()
