# Arquitetura do Sistema - AIBOT Trade Copier

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AIBOT TRADE COPIER                          │
│                     Arquitetura Cliente-Servidor                    │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│   MT5 MASTER     │         │   API SERVER     │         │   MT5 CLIENT     │
│   (Conta Mestre) │         │   (Rust/Axum)    │         │  (Conta Copier)  │
└────────┬─────────┘         └────────┬─────────┘         └────────▲─────────┘
         │                            │                            │
         │ Monitora                   │ HTTP/WebSocket             │ Copia
         │ Ordens                     │ Port: 8000                 │ Ordens
         │                            │                            │
         ▼                            │                            │
┌──────────────────┐                  │                   ┌──────────────────┐
│ MASTER SENDER    │                  │                   │ CLIENT COPIER    │
│ (Python EXE)     │                  │                   │ (Python EXE)     │
│                  │                  │                   │                  │
│ • Lê MT5 Master  │──────HTTP POST──▶│                   │                  │
│ • Detecta novas  │   /signal/       │                   │                  │
│   ordens         │   broadcast      │                   │                  │
│ • Envia para API │                  │◀──WebSocket (/ws)─┤ • Conecta WS     │
│                  │                  │                   │ • Recebe ordens  │
│ Logs:            │                  │                   │ • Copia no MT5   │
│ sender.log       │                  │                   │                  │
└──────────────────┘                  │                   │ Logs:            │
         │                            │                   │ client.log       │
         │                            │                   └──────────────────┘
         │                            │
         │                            │
         ▼                            ▼
┌──────────────────┐         ┌──────────────────┐
│ config_sender    │         │ SQLite Database  │
│ .json            │         │ • Users          │
│                  │         │ • Signals        │
│ • API URL        │         │ • Configs        │
│ • MT5 Creds      │         └──────────────────┘
└──────────────────┘


═══════════════════════════════════════════════════════════════════════
                           FLUXO DE DADOS
═══════════════════════════════════════════════════════════════════════

1. DETECÇÃO DE ORDEM (Master Sender)
   ┌─────────────────────────────────────────────────────────────┐
   │ MT5 Master → Master Sender detecta nova ordem               │
   │ • Ticket: 123456                                            │
   │ • Symbol: EURUSD                                            │
   │ • Type: BUY                                                 │
   │ • Volume: 0.10                                              │
   │ • Price: 1.0850                                             │
   │ • SL: 1.0800                                                │
   │ • TP: 1.0900                                                │
   └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
2. ENVIO PARA API (HTTP POST)
   ┌─────────────────────────────────────────────────────────────┐
   │ POST http://localhost:8000/signal/broadcast                 │
   │ Headers:                                                    │
   │   Authorization: Bearer <token>                             │
   │ Body:                                                       │
   │   {                                                         │
   │     "symbol": "EURUSD",                                     │
   │     "action": "BUY",                                        │
   │     "volume": 0.10,                                         │
   │     "price": 1.0850,                                        │
   │     "sl": 1.0800,                                           │
   │     "tp": 1.0900                                            │
   │   }                                                         │
   └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
3. PROCESSAMENTO NO SERVIDOR (Rust)
   ┌─────────────────────────────────────────────────────────────┐
   │ • Valida autenticação                                       │
   │ • Salva no banco de dados                                   │
   │ • Envia via broadcast channel para todos os clientes WS     │
   └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
4. RECEBIMENTO VIA WEBSOCKET (Client Copier)
   ┌─────────────────────────────────────────────────────────────┐
   │ WebSocket Message Received:                                 │
   │ {                                                           │
   │   "type": "signal",                                         │
   │   "data": {                                                 │
   │     "symbol": "EURUSD",                                     │
   │     "action": "BUY",                                        │
   │     "volume": 0.01,  // Ajustado pelo config               │
   │     "price": 1.0850,                                        │
   │     "sl": 1.0800,                                           │
   │     "tp": 1.0900                                            │
   │   }                                                         │
   │ }                                                           │
   └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
5. EXECUÇÃO NO MT5 CLIENT
   ┌─────────────────────────────────────────────────────────────┐
   │ Client Copier executa:                                      │
   │ • Verifica safety rules (spread, slippage, exposure)        │
   │ • Ajusta volume conforme config (fix/multiplier)            │
   │ • Envia ordem para MT5 Client                               │
   │ • Salva mapeamento ticket_master → ticket_client            │
   └─────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════
                        ARQUIVOS DE CONFIGURAÇÃO
═══════════════════════════════════════════════════════════════════════

config_sender.json (Master)
────────────────────────────
{
  "api": {
    "url": "http://127.0.0.1:8000",
    "username": "master_user",
    "password": "secret_password"
  },
  "mt5": {
    "login": 12345678,
    "password": "mt5_password",
    "server": "Broker-Server"
  }
}

config_client.json (Client)
────────────────────────────
{
  "api": {
    "url": "http://127.0.0.1:8000",
    "ws_url": "ws://127.0.0.1:8000",
    "username": "client_user",
    "password": "client_password"
  },
  "mt5": {
    "login": 87654321,
    "password": "mt5_password",
    "server": "Broker-Server"
  },
  "trade_copy": {
    "mode": "fix",              // "fix" ou "multiplier"
    "fixed_lot": 0.01,          // Volume fixo se mode = "fix"
    "multiplier": 1.0,          // Multiplicador se mode = "multiplier"
    "magic_number_copier": 123456,
    "max_slippage_points": 50,
    "max_spread_points": 20,
    "max_exposure_trades": 5,
    "max_exposure_lots": 10.0
  }
}


═══════════════════════════════════════════════════════════════════════
                           ENDPOINTS DA API
═══════════════════════════════════════════════════════════════════════

Públicos:
─────────
POST /token                    → Login (retorna JWT token)
POST /users/public             → Criar usuário público

Protegidos (requer Bearer token):
──────────────────────────────────
POST /users/                   → Criar usuário (admin)
POST /users/config             → Atualizar configuração
POST /signal/broadcast         → Enviar sinal (Master Sender)
POST /signal/close             → Fechar sinal
GET  /ws                       → WebSocket (Client Copier)
GET  /health                   → Health check


═══════════════════════════════════════════════════════════════════════
                         SEGURANÇA E PROTEÇÃO
═══════════════════════════════════════════════════════════════════════

1. Autenticação JWT
   • Master e Client fazem login via POST /token
   • Recebem JWT token
   • Incluem token em todas as requisições

2. Proteção dos Executáveis
   • PyInstaller com --onefile (código empacotado)
   • Opção --key para ofuscação básica
   • Para produção: usar PyArmor para proteção avançada

3. Safety Rules (Client)
   • Max slippage: 50 points
   • Max spread: 20 points
   • Max exposure: 5 trades ou 10.0 lots
   • Max drawdown: 10%

4. Validações
   • Verificação de símbolo disponível
   • Verificação de margem
   • Verificação de volume mínimo/máximo


═══════════════════════════════════════════════════════════════════════
                            LOGS E DEBUG
═══════════════════════════════════════════════════════════════════════

Master Sender:
──────────────
sender.log
• Ordens detectadas no MT5 Master
• Requisições HTTP enviadas
• Respostas da API
• Erros de conexão

Client Copier:
──────────────
client.log
• Conexão WebSocket
• Sinais recebidos
• Ordens executadas no MT5 Client
• Safety rules aplicadas
• Erros de execução

API Server:
───────────
Console output (tracing)
• Requisições HTTP recebidas
• WebSocket connections
• Database operations
• Broadcast messages
