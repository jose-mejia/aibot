# 🌐 ZulFinance Integration Guide
**Backend Rust 🔗 Admin Panel Frontend**

Integração concluída com sucesso. O frontend agora consome diretamente a API Server Rust.

---

## ✅ Status da Integração

| Componente | Status | Detalhes |
|------------|--------|----------|
| **Login** | ✅ Conectado | Frontend usa `api.login` e armazena JWT Token |
| **Users** | ✅ Conectado | Dashboard lista usuários via `/users` |
| **Create User** | ✅ Conectado | Criação de usuários via `/users` (hash automático) |
| **Signals** | ✅ Conectado | Monitor de sinais consome `/signals` |
| **Security** | ✅ Ativo | Todos requests usam `Authorization: Bearer <token>` |

---

## 🚀 Como Rodar o Sistema Completo

### 1. Iniciar o Backend (API Server)
Abra um terminal (`cmd` ou `powershell`):
```bash
cd c:\Users\josemejia\dev\python\aibot\backend\copy
./api_server/target/release/api_server_rust.exe
```
*Deve aparecer: `Server listening on 0.0.0.0:8000`*

### 2. Iniciar o Frontend (Admin Panel)
Abra **outro** terminal:
```bash
cd c:\Users\josemejia\dev\python\aibot\backend\copy\api_server\admin_panel
npx vite
```
*Deve aparecer: `Local: http://localhost:5173/`*

### 3. Acessar
Abra o navegador em `http://localhost:5173`

- **Login:** `admin`
- **Senha:** `admin123`

---

## 🧪 Testes Realizados

1. **Login Flow:**
   - Frontend envia credenciais `POST /token`
   - Backend valida e retorna JWT
   - Frontend salva token e redireciona para Dashboard

2. **Data Loading:**
   - Dashboard chama `GET /users` com token
   - Backend retorna lista de usuários do SQLite
   - Frontend renderiza tabela

3. **Signal Monitoring:**
   - SignalMonitor chama `GET /signals` com token
   - Frontend mapeia resposta do Rust para interface visual

---

## ⚠️ Notas Importantes

- O backend Rust é a única fonte de verdade. Não há mocks.
- Se o backend for reiniciado, o token atual pode continuar válido (JWT stateless), mas novos dados serão perdidos se o banco for em memória (que não é o caso, usamos SQLite persistente `aibot.db`).
- Se precisar limpar o banco, delete o arquivo `aibot.db` na raiz.

**Integração Finalizada!** 🎉
