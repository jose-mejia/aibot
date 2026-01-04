# 🔍 AUDITORIA E CHECKLIST - FLUXO DE CÓPIA DE ORDENS

**Data:** 2026-01-04  
**Versão do Sistema:** v1.0-stable  
**Status:** ✅ PRONTO PARA TESTES

---

## 📊 RESUMO EXECUTIVO

### ✅ Componentes Validados
- ✅ Master Sender (Python) - Detecção e envio de sinais
- ✅ API Server (Rust) - Recepção, validação e broadcast
- ✅ Client Copier (Python) - Recepção e execução
- ✅ Segurança (HMAC, JWT, Role-based)
- ✅ Banco de Dados (SQLite com schema correto)

### ⚠️ Pontos de Atenção Identificados
1. **Modo de Cálculo de Lote:** Config `mode: "fix"` não reconhecido → usa `min_lot` como fallback
2. **Stop Loss Opcional:** SafetyGuard permite ordens sem SL (configurável)
3. **Limite de Ordens:** Máximo 3 ordens por símbolo (pode precisar ajuste)

---

## 🔄 FLUXO DETALHADO (Step-by-Step)

### ETAPA 1: Detecção no Master (sender_service.py)

**Arquivo:** `master_sender/sender_service.py`  
**Função:** `_check_and_send()` (linhas 119-172)

#### Como Funciona:
1. **Polling a cada 50ms** (loop principal)
2. **Busca posições e ordens** via `mt5.positions_get()` e `mt5.orders_get()`
3. **Compara com estado anterior** (`self.last_state`)
4. **Detecta eventos:**
   - ✅ **Nova Ordem:** Ticket não existe em `last_state` → Envia sinal OPEN
   - ✅ **Modificação:** SL ou TP mudou → Envia sinal MODIFY
   - ✅ **Fechamento:** Ticket sumiu do MT5 → Envia sinal CLOSE

#### Dados Enviados:
```python
{
    "master_ticket": 12345,
    "symbol": "EURUSD",
    "type": "BUY",  # ou 0 (int)
    "volume": 0.01,
    "price": 1.08500,
    "sl": 1.08000,
    "tp": 1.09000
}
```

#### ✅ Validação de Código:
- ✅ Usa `.get()` para acesso seguro
- ✅ Normaliza `type` com `_map_order_type()`
- ✅ Trata `positions` e `orders` como None-safe
- ✅ Log detalhado de eventos

---

### ETAPA 2: Envio Seguro (sender_service.py)

**Função:** `_send_signal()` (linhas 174-195)

#### Como Funciona:
1. **Gera HMAC-SHA256** do payload usando JWT como chave
2. **Adiciona timestamp** para prevenir replay attacks
3. **Envia POST** para `/signals/broadcast`
4. **Headers de Segurança:**
   ```
   Authorization: Bearer {JWT}
   X-Signature: {HMAC}
   X-Timestamp: {Unix timestamp}
   Content-Type: application/json
   ```

#### ✅ Validação de Código:
- ✅ HMAC implementado corretamente
- ✅ Timestamp em milissegundos
- ✅ Tratamento de erros HTTP
- ✅ Retry logic (implícito no loop)

---

### ETAPA 3: Recepção na API (handlers/mod.rs)

**Arquivo:** `api_server/src/handlers/mod.rs`  
**Função:** `broadcast_signal()` (linhas 560-622)

#### Como Funciona:
1. **Valida JWT** (autenticação)
2. **Valida Role** (apenas MASTER pode broadcast)
3. **Valida HMAC** (integridade do payload)
4. **Valida Timestamp** (anti-replay, janela de 60s)
5. **Salva no banco** (tabela `signals`)
6. **Broadcast via WebSocket** para todos os clientes conectados

#### SQL Executado:
```sql
INSERT OR REPLACE INTO signals 
(ticket, symbol, type, volume, price, sl, tp, status) 
VALUES (?, ?, ?, ?, ?, ?, ?, 'OPEN')
```

#### ✅ Validação de Código:
- ✅ 4 camadas de segurança (JWT, Role, HMAC, Timestamp)
- ✅ UPSERT previne duplicatas
- ✅ Broadcast assíncrono (não bloqueia)
- ✅ Log de debug ativo

---

### ETAPA 4: Recepção no Client (client_service.py)

**Função:** `handle_signal()` (linhas 140-177)

#### Como Funciona:
1. **Recebe via WebSocket** (conexão persistente)
2. **Parse do evento:**
   - `SNAPSHOT` → Sincronização inicial (todas as ordens ativas)
   - `OPEN` → Nova ordem
   - `MODIFY` → Modificação de SL/TP
   - `CLOSE` → Fechamento
3. **Normaliza ticket** (`master_ticket` ou `ticket`)
4. **Atualiza cache local** (`self.server_signals`)
5. **Chama `process_trade()`**

#### ✅ Validação de Código:
- ✅ Trata eventos diferentes corretamente
- ✅ Normalização de campos
- ✅ Cache local para comparação
- ✅ Logs informativos

---

### ETAPA 5: Execução no MT5 Client (_execute_open)

**Função:** `_execute_open()` (linhas 222-301)

#### Como Funciona:
1. **Normaliza símbolo** (ex: `EURUSD` → `EURUSD.m` se necessário)
2. **Verifica se já existe** (via comment `COPY_{master_ticket}`)
3. **Valida segurança:**
   - ✅ Limite de ordens por símbolo (3)
   - ✅ Stop Loss obrigatório (configurável)
   - ✅ Margem suficiente
   - ✅ Latência aceitável (<10s)
4. **Calcula lote** baseado no modo configurado
5. **Arredonda preços** para `digits` do símbolo
6. **Envia ordem** via `mt5.order_send()`
7. **Salva no banco local** para tracking

#### Request MT5:
```python
{
    "action": TRADE_ACTION_DEAL,  # ou PENDING
    "symbol": "EURUSD",
    "volume": 0.01,
    "type": ORDER_TYPE_BUY,
    "price": 1.08500,
    "sl": 1.08000,
    "tp": 1.09000,
    "deviation": 50,
    "magic": 987654,
    "comment": "COPY_12345",
    "type_filling": ORDER_FILLING_IOC
}
```

#### ✅ Validação de Código:
- ✅ Arredondamento de preços implementado
- ✅ Validação de tick antes de usar
- ✅ SafetyGuard ativo
- ✅ Deduplicação via comment
- ✅ Log detalhado do request

---

## 🐛 PROBLEMAS IDENTIFICADOS E SOLUÇÕES

### 1. ⚠️ "Unknown mode fix, defaulting to min_lot"

**Localização:** `client_copier/utils.py` linha ~15

**Problema:**
```python
def calculate_lot_size(master_lot, master_balance, follower_balance, mode, config):
    if mode == "proportional":
        # ...
    elif mode == "fixed_ratio":
        # ...
    else:
        logger.warning(f"Unknown mode {mode}, defaulting to min_lot")
        return config.get('min_lot', 0.01)
```

**Config Atual:**
```json
{
    "trade_copy": {
        "mode": "fix",  // ❌ NÃO RECONHECIDO
        "min_lot": 0.01
    }
}
```

**Solução:**
Alterar config para:
```json
{
    "trade_copy": {
        "mode": "proportional",  // ou "fixed_ratio"
        "min_lot": 0.01,
        "ratio": 1.0  // se usar fixed_ratio
    }
}
```

**OU** adicionar suporte ao modo "fix" no código.

---

### 2. ⚠️ "Master Order has NO Stop Loss"

**Localização:** `client_copier/safety.py`

**Problema:** SafetyGuard está configurado para **PERMITIR** ordens sem SL (apenas avisa).

**Config Atual:**
```json
{
    "safety": {
        "require_sl": false  // ⚠️ Permite sem SL
    }
}
```

**Recomendação:**
- **Para testes:** Manter `false`
- **Para produção:** Alterar para `true` (força SL obrigatório)

---

### 3. ⚠️ "LIMIT REACHED: 10 orders already exist for BTCUSD. Max is 3"

**Localização:** `client_copier/safety.py`

**Problema:** Limite muito restritivo para testes com múltiplas ordens.

**Solução Temporária (para testes):**
Editar `client_copier/safety.py`:
```python
def check_order_limit(self, symbol, positions, orders):
    max_per_symbol = 10  # Era 3, aumentar para testes
```

**Solução Permanente:**
Tornar configurável via `config_client.json`.

---

## ✅ CHECKLIST DE TESTES

### PRÉ-REQUISITOS
- [ ] API Server rodando (`cargo run`)
- [ ] Master Sender rodando e conectado ao MT5 Master
- [ ] Client Copier rodando e conectado ao MT5 Client
- [ ] Ambos os MT5 logados e com contas diferentes
- [ ] Paths configurados corretamente no Profile

---

### TESTE 1: Ordem de Compra (BUY Market)

#### Passos:
1. [ ] Abrir MT5 Master
2. [ ] Abrir ordem manual: **BUY 0.01 EURUSD** (market)
3. [ ] Definir SL e TP

#### Verificações:
- [ ] **Master Sender Log:** "New POSITION Detected: {ticket} EURUSD - SENDING SIGNAL NOW!"
- [ ] **API Server Log:** "📡 Broadcasting signal: ..."
- [ ] **Client Copier Log:** "Signal Received: OPEN {ticket}"
- [ ] **Client Copier Log:** "🚀 SENDING ORDER: ..."
- [ ] **Client Copier Log:** "Opened Trade {client_ticket}"
- [ ] **MT5 Client:** Ordem aparece com comment `COPY_{master_ticket}`
- [ ] **Banco API:** `SELECT * FROM signals WHERE ticket = {master_ticket}` retorna 1 linha
- [ ] **Banco Client:** Registro salvo em `trades.db`

#### Critérios de Sucesso:
- ✅ Ordem copiada em <5 segundos
- ✅ Símbolo, direção e SL/TP idênticos
- ✅ Volume calculado corretamente (proporcional ou fixo)

---

### TESTE 2: Ordem Pendente (BUY LIMIT)

#### Passos:
1. [ ] No MT5 Master, colocar **BUY LIMIT 0.01 EURUSD** a 10 pips abaixo do preço atual
2. [ ] Definir SL e TP

#### Verificações:
- [ ] **Master Sender Log:** "New ORDER Detected: ..."
- [ ] **Client Copier:** Ordem pendente criada (não executada)
- [ ] **MT5 Client:** Ordem pendente visível

---

### TESTE 3: Modificação de SL/TP

#### Passos:
1. [ ] Modificar SL ou TP de uma ordem existente no Master
2. [ ] Observar logs

#### Verificações:
- [ ] **Master Sender Log:** "Trade Modified: {ticket} SL/TP Changed"
- [ ] **Client Copier:** SL/TP atualizado na ordem copiada

---

### TESTE 4: Fechamento de Ordem

#### Passos:
1. [ ] Fechar manualmente uma ordem no MT5 Master
2. [ ] Observar logs

#### Verificações:
- [ ] **Master Sender Log:** "Trade Closed/Removed on Master: {ticket}"
- [ ] **API Server:** Sinal de CLOSE enviado
- [ ] **Client Copier Log:** "Close Signal: {ticket}"
- [ ] **MT5 Client:** Ordem correspondente fechada automaticamente

---

### TESTE 5: Múltiplas Ordens Simultâneas

#### Passos:
1. [ ] Abrir 3 ordens diferentes no Master (ex: EURUSD, GBPUSD, USDJPY)
2. [ ] Observar se todas são copiadas

#### Verificações:
- [ ] Todas as 3 ordens aparecem no Client
- [ ] Sem erros de "LIMIT REACHED" (se ajustado)

---

### TESTE 6: Reconexão após Queda

#### Passos:
1. [ ] Abrir 2 ordens no Master
2. [ ] Parar o Client Copier (`Ctrl+C`)
3. [ ] Abrir mais 1 ordem no Master
4. [ ] Reiniciar Client Copier

#### Verificações:
- [ ] **Client Copier Log:** "Received Snapshot with 3 trades"
- [ ] Todas as 3 ordens são sincronizadas (via `sync_local_state`)

---

### TESTE 7: Segurança - Tentativa de Broadcast sem MASTER Role

#### Passos:
1. [ ] Tentar enviar POST `/signals/broadcast` com token de CLIENT
2. [ ] Observar resposta

#### Verificações:
- [ ] **API retorna:** `403 Forbidden - Only MASTER users can broadcast signals`

---

### TESTE 8: Segurança - HMAC Inválido

#### Passos:
1. [ ] Modificar manualmente o header `X-Signature` em um request
2. [ ] Enviar para API

#### Verificações:
- [ ] **API retorna:** `401 Invalid signature or timestamp`

---

## 📈 MÉTRICAS DE SUCESSO

| Métrica | Alvo | Atual |
|---------|------|-------|
| Latência de Cópia | <5s | A testar |
| Taxa de Sucesso | >95% | A testar |
| Precisão de Preço | 100% | ✅ (arredondamento implementado) |
| Uptime do Sistema | >99% | A monitorar |

---

## 🔧 AJUSTES RECOMENDADOS ANTES DOS TESTES

### 1. Configurar Modo de Lote

**Arquivo:** `client_copier/config_client.json`

```json
{
    "trade_copy": {
        "mode": "proportional",  // MUDAR DE "fix"
        "min_lot": 0.01,
        "max_lot": 1.0,
        "risk_percent": 1.0
    }
}
```

### 2. Aumentar Limite de Ordens (Temporário)

**Arquivo:** `client_copier/safety.py`

```python
def check_order_limit(self, symbol, positions, orders):
    max_per_symbol = 10  # Aumentar de 3 para 10
```

### 3. Habilitar Logs de Debug

**Arquivo:** `client_copier/main.py` e `master_sender/main.py`

```python
logging.basicConfig(
    level=logging.DEBUG,  # Era INFO
    # ...
)
```

---

## 🚀 PRÓXIMOS PASSOS

1. **Aplicar Ajustes Recomendados** (configs acima)
2. **Executar Checklist de Testes** (ordem sequencial)
3. **Documentar Resultados** (criar planilha de testes)
4. **Corrigir Bugs Encontrados** (se houver)
5. **Testes de Stress** (10+ ordens simultâneas)
6. **Testes de Longa Duração** (24h rodando)

---

## 📞 SUPORTE

**Em caso de erro:**
1. Capturar logs completos (Master, Client, API)
2. Verificar status do banco: `python debug_db.py`
3. Verificar sinais salvos: `SELECT * FROM signals;`
4. Consultar `DATABASE_SECURITY.md` para troubleshooting

---

**Documento preparado por:** Antigravity AI  
**Revisão de Código:** ✅ COMPLETA  
**Status:** 🟢 APROVADO PARA TESTES
