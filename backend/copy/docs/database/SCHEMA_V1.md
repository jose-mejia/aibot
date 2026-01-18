# 🗄️ Esquema do Banco de Dados (Database Schema)
**Status:** V1.0 - Produção
**Arquivo Físico:** `api_server/aibot.db` (SQLite)
**Responsável:** API Server (Rust) - Único ponto de escrita.

---

## 1. Tabela `users`
Armazena as credenciais de acesso e a configuração de conexão MT5 de cada usuário.

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | INTEGER PK | Identificador único do usuário. |
| `username` | TEXT | Nome de login (ex: `admin`, `master`, `client`). |
| `password_hash` | TEXT | Hash da senha (Bcrypt). |
| `role` | TEXT | Nível de acesso: `ADMIN`, `MASTER`, `FOLLOWER`. |
| `allowed_mt5_id` | INTEGER | **(Crítico)** ID da conta MT5 permitida para este usuário. |
| `mt5_path` | TEXT | **(Crítico)** Caminho absoluto do `terminal64.exe` correto. |
| `created_at` | DATETIME | Data de criação do registro. |

### Dados Iniciais (Seed)
- **Master:** ID 3 | MT5 ID: `7409735`
- **Client:** ID 2 | MT5 ID: `11629107`

---

## 2. Tabela `signals`
Armazena todos os sinais de trading detectados pelo Master e distribuídos para os Clients.

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | INTEGER PK | Identificador sequencial do sinal. |
| `ticket` | INTEGER | Ticket original da ordem no MT5 do Master. |
| `symbol` | TEXT | Ativo negociado (ex: `BTCUSD`). |
| `type` | TEXT | Tipo de ordem (`BUY`, `SELL`, `BUY_LIMIT`, etc). |
| `volume` | REAL | Lote original da ordem. |
| `price` | REAL | Preço de entrada. |
| `sl` | REAL | Stop Loss. |
| `tp` | REAL | Take Profit. |
| `status` | TEXT | Estado do sinal: `OPEN`, `CLOSED`, `MODIFIED`. |
| `timestamp` | DATETIME | Hora exata da detecção. |

---

## 📊 Relacionamentos e Fluxo
1. **Master Sender:** Lê o banco (via API) para saber qual `mt5_path` usar.
2. **Master Sender:** Envia dados para a API, que grava na tabela `signals`.
3. **Client Copier:** Lê a tabela `signals` (via API) para copiar as operações.
