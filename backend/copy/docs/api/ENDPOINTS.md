# 🌐 API Server Endpoints
**Base URL:** `http://127.0.0.1:8000`
**Tecnologia:** Rust (Axum)
**Autenticação:** Bearer Token (JWT) no header `Authorization`.

---

## 🔐 Autenticação

### `POST /token`
Realiza o login e retorna o token JWT.
- **Body:**
  ```json
  {
    "username": "master",
    "password": "123"
  }
  ```
- **Response (200 OK):** "eyJhbGciOiJIUzI1Ni..." (String pura do token)

---

## 👤 Usuários & Configuração

### `GET /users/me`
Retorna os dados do usuário logado, incluindo configurações críticas de MT5.
- **Header:** `Authorization: Bearer <token>`
- **Response:**
  ```json
  {
    "id": 2,
    "username": "client",
    "role": "FOLLOWER",
    "allowed_mt5_id": 11629107,
    "mt5_path": "C:\\Program Files\\..."
  }
  ```

### `GET /users/config`
Retorna configurações globais do sistema (ex: pares permitidos, riscos).
- **Header:** `Authorization: Bearer <token>`

---

## 📡 Sinais (Signals)

### `POST /signal`
Usado pelo **Master Sender** para registrar uma nova ordem ou modificação.
- **Header:** `Authorization: Bearer <token>`
- **Body:**
  ```json
  {
    "ticket": 123456,
    "symbol": "BTCUSD",
    "type": "BUY",
    "volume": 0.1,
    "price": 50000.0,
    "sl": 49000.0,
    "tp": 55000.0,
    "status": "OPEN"
  }
  ```

### `WS /ws` (WebSocket)
Conexão persistente para receber sinais em tempo real.
- **Query Param:** `?token=<jwt_token>`
- **Fluxo:** O servidor faz broadcast de qualquer sinal recebido via `POST /signal` para todos os clientes conectados neste socket.

---

## 📊 Status do MT5

### `POST /mt5/status`
Atualiza o estado atual da conta (saldo, equity).
- **Body:**
  ```json
  {
    "login": 11629107,
    "balance": 1000.0,
    "equity": 1050.0
  }
  ```
