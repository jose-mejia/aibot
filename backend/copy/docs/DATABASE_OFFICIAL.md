# 🗄️ BANCO DE DADOS OFICIAL

## ⚠️ IMPORTANTE - LEIA PRIMEIRO

**EXISTE APENAS UM BANCO DE DADOS OFICIAL:**

```
api_server/aibot.db
```

**NUNCA** use ou crie outros arquivos `.db`. Qualquer referência a `users.db` ou outros bancos é **OBSOLETA** e foi removida.

---

## 🏗️ Arquitetura de Acesso

### ✅ REGRA DE OURO: Apenas a API acessa o banco

```
Desktop Apps (Master/Client)
         │
         │ HTTP/WebSocket (API Calls)
         │
         ▼
    API Server (Rust) ◄──── ÚNICA CONEXÃO DIRETA
         │
         │ SQLite
         ▼
    aibot.db
```

**NUNCA:**
- ❌ Desktop apps NÃO acessam o banco diretamente
- ❌ Python services NÃO acessam o banco diretamente
- ❌ Frontend NÃO acessa o banco diretamente

**SEMPRE:**
- ✅ Toda operação de dados passa pela API REST
- ✅ API é a única camada com acesso ao SQLite
- ✅ Segurança, validação e lógica de negócio na API

### 🛠️ Exceção: Scripts Administrativos

Scripts Python (`debug_db.py`, `reset_passwords.py`, etc.) são **ferramentas de manutenção** para uso administrativo local, NÃO fazem parte da aplicação em produção.

---

## 📍 Localização

- **Caminho Absoluto:** `C:\Users\josemejia\dev\python\aibot\backend\copy\api_server\aibot.db`
- **Caminho Relativo (do root do projeto):** `api_server/aibot.db`

---

## 🔧 Scripts de Manutenção

Todos os scripts Python foram atualizados para usar `aibot.db`:

| Script | Função |
|--------|--------|
| `debug_db.py` | Visualizar usuários e configurações |
| `reset_passwords.py` | Resetar senhas dos usuários de teste |
| `migrate_db_path.py` | Adicionar coluna `mt5_path` (já executado) |
| `fix_client_db.py` | Corrigir MT5 ID do cliente |
| `fix_master_id.py` | Corrigir MT5 ID do master |
| `fix_db_schema.py` | Adicionar coluna `allowed_mt5_id` |

---

## 🔐 Usuários Padrão

```
Admin:  admin  / admin123
Master: master / 123123
Client: client / 123123
```

---

## 📊 Schema Atual

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    phone TEXT,
    hashed_password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'FOLLOWER',
    status TEXT NOT NULL DEFAULT 'ACTIVE',
    allowed_mt5_id TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    mt5_path TEXT DEFAULT ''
);
```

---

## ⚙️ Configuração da API

O servidor Rust (`api_server`) está configurado para usar `aibot.db` via:

```rust
// src/db/mod.rs
let db_url = env::var("DATABASE_URL").unwrap_or("sqlite:aibot.db".to_string());
```

**Não altere isso.** Se precisar usar outro banco (ex: produção), defina a variável de ambiente `DATABASE_URL`.

---

## 🚨 Troubleshooting

### "No such column: mt5_path"
Execute: `python migrate_db_path.py`

### "Invalid credentials"
Execute: `python reset_passwords.py`

### "Wrong Account!"
Execute: `python fix_client_db.py` ou `python fix_master_id.py`

---

## 🔒 Backup

Antes de qualquer operação destrutiva, faça backup:

```powershell
Copy-Item "api_server\aibot.db" "api_server\aibot.db.backup"
```

---

**Última atualização:** 2026-01-04
**Versão do Schema:** 1.1 (com mt5_path)
