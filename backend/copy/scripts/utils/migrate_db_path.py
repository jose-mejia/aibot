import sqlite3
import os

db_path = 'api_server/aibot.db'

if not os.path.exists(db_path):
    print(f"❌ Banco de dados não encontrado em: {db_path}")
    exit(1)

print(f"🔧 Conectando ao banco: {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Tenta adicionar a coluna
    cursor.execute("ALTER TABLE users ADD COLUMN mt5_path TEXT DEFAULT ''")
    print("✅ Coluna 'mt5_path' adicionada com sucesso!")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("⚠️ Coluna 'mt5_path' já existe. Nenhuma ação necessária.")
    else:
        print(f"❌ Erro ao alterar tabela: {e}")

# Opcional: Pré-popular com valores padrão para seus testes locais se quiser
# (Isso ajuda vc a testar sem precisar preencher a UI agora mesmo)
# cursor.execute("UPDATE users SET mt5_path = 'C:\\Program Files\\MetaTrader 5\\terminal64.exe' WHERE username='client'")
# cursor.execute("UPDATE users SET mt5_path = 'C:\\Program Files\\ICMarkets MT5\\terminal64.exe' WHERE username='master'")

conn.commit()

# Verificar schema
cursor.execute("PRAGMA table_info(users)")
columns = [info[1] for info in cursor.fetchall()]
print(f"📊 Colunas atuais na tabela 'users': {columns}")

conn.close()
