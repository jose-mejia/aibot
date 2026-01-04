import sqlite3
import bcrypt

# Conectar ao banco de dados
db_path = 'api_server/aibot.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Garantir que a tabela existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'FOLLOWER',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
''')
print("✅ Tabela 'users' verificada/criada.")

# Senhas padrão para teste
users = [
    ('admin', 'admin123', 'ADMIN'),
    ('master', 'master123', 'MASTER'),
    ('client', 'client123', 'FOLLOWER')
]

print("\n🔄 Inserindo/Atualizando usuários...\n")

for username, password, role in users:
    # Gerar hash bcrypt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
    password_hash = hashed.decode('utf-8')
    
    # Tentar inserir ou atualizar
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        print(f"✅ Usuário '{username}' CRIADO com sucesso.")
    except sqlite3.IntegrityError:
        # Se já existe, atualiza a senha
        cursor.execute(
            "UPDATE users SET password_hash = ?, role = ? WHERE username = ?",
            (password_hash, role, username)
        )
        print(f"✅ Usuário '{username}' ATUALIZADO com nova senha.")

conn.commit()
conn.close()

print("\n🎉 Banco de dados pronto!")
print("\n📋 Credenciais Válidas:")
print("=" * 40)
for username, password, role in users:
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Role: {role}")
    print("-" * 40)
