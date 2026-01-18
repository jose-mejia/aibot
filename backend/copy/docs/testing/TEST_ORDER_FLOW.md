# 🧪 Teste de Validação: Master → Client Order Flow

**Data:** 2026-01-05 11:25  
**Objetivo:** Validar que apps Python estão funcionando corretamente antes de escalar para dev backend (API Rust).

---

## ✅ Checklist de Validação

### Pré-Requisitos
- [ ] API Server rodando (`http://localhost:8000`)
- [ ] Master Sender conectado ao MT5 (7409735)
- [ ] Client Copier conectado ao MT5 (11629107)
- [ ] Ambos conectados ao WebSocket

### Teste 1: Abertura de Ordem no Master

**Ação:** Abrir ordem MANUAL no MT5 do Master

**Validações no Master Sender:**
- [ ] Log: "New POSITION Detected: {ticket}"
- [ ] Log: "Signal broadcast successfully: {ticket}"
- [ ] HTTP Status: 200 (não 401, 403, ou 500)

**Validações no Client Copier:**
- [ ] Log: "Signal Received: OPEN {ticket}"
- [ ] Log: "SENDING ORDER: {'action': ...}"
- [ ] Ordem executada no MT5 do Client (verificar visualmente)
- [ ] Sem erro "10015 - Invalid price"
- [ ] Sem erro "10016 - Invalid stops"

### Teste 2: Modificação de SL/TP

**Ação:** Modificar SL ou TP da ordem no Master

**Validações no Master Sender:**
- [ ] Log: "Trade Modified: {ticket} SL/TP Changed"
- [ ] Log: "Signal broadcast successfully: {ticket}"

**Validações no Client Copier:**
- [ ] Log: "Signal Received: MODIFY {ticket}"
- [ ] SL/TP atualizado no MT5 do Client

### Teste 3: Fechamento de Ordem

**Ação:** Fechar ordem no Master

**Validações no Master Sender:**
- [ ] Log: "Trade Closed/Removed on Master: {ticket}"
- [ ] Chamada a `_send_close(ticket)`

**Validações no Client Copier:**
- [ ] Log: "Close Signal: {ticket}"
- [ ] Ordem fechada no MT5 do Client

---

## 📋 Comandos de Monitoramento

### Iniciar Apps (se não estiverem rodando)

**Master Sender:**
```powershell
cd master_sender\gui
npm run tauri dev
```

**Client Copier:**
```powershell
cd client_copier\gui
npm run tauri dev
```

**API Server:**
```powershell
cd api_server
cargo run
```

### Monitorar Logs em Tempo Real

**Opção 1: Console do Tauri**
- Abrir DevTools no app (F12)
- Aba "Console" → Ver logs do Python

**Opção 2: Arquivo de Log (se configurado)**
```powershell
# Master
Get-Content master_sender\logs\sender.log -Wait -Tail 20

# Client
Get-Content client_copier\logs\client.log -Wait -Tail 20
```

---

## 🔍 Pontos Críticos a Observar

### 1. Master Sender

**Logs Esperados (SUCESSO):**
```
INFO - New POSITION Detected: 123456 EURUSD - SENDING SIGNAL NOW!
INFO - Signal broadcast successfully: 123456
```

**Logs de ERRO (PROBLEMA):**
```
ERROR - Failed to broadcast signal: {error_message}
CRITICAL - SECURITY ALERT: Token Rejected
```

### 2. Client Copier

**Logs Esperados (SUCESSO):**
```
INFO - Signal Received: OPEN 123456
INFO - SENDING ORDER: {'action': 1, 'symbol': 'EURUSD', ...}
INFO - Trade opened successfully: Follower ticket 789012
```

**Logs de ERRO (PROBLEMA NO PYTHON):**
```
ERROR - Trade Execution Failed: 10015 - Invalid price
ERROR - Trade Execution Failed: 10016 - Invalid stops
ERROR - Error processing signal: {exception}
```

**Logs de ERRO (PROBLEMA NA API):**
```
ERROR - MT5 status not available (404)
ERROR - Connection Lost: Code=1008
CRITICAL - SESSION EXPIRED or INVALID TOKEN
```

### 3. API Server

**Logs Esperados (SUCESSO):**
```
📥 MT5 Status Update from User 3: {...}
DEBUG request{method=POST uri=/signal/broadcast}: finished processing request latency=X ms status=200
```

**Logs de ERRO (PROBLEMA NA API):**
```
ERROR - Failed to broadcast signal
status=500 Internal Server Error
```

---

## 🎯 Critérios de Sucesso

### ✅ Apps Python OK (pode escalar para backend)
- Master detecta ordem e envia sinal (HTTP 200)
- Client recebe sinal via WebSocket
- Client executa ordem no MT5 (sem erro 10015/10016)
- Logs mostram fluxo completo sem exceções Python

### ❌ Apps Python com Problema (NÃO escalar ainda)
- Master não detecta ordem
- Master envia sinal mas recebe erro HTTP (401, 403, 500)
- Client não recebe sinal (WebSocket desconectado)
- Client recebe sinal mas falha ao executar (erro 10015/10016)
- Exceções Python nos logs

---

## 📊 Formato de Reporte

### Se Tudo OK:
```
✅ APPS PYTHON VALIDADOS

Master Sender:
- Ordem detectada: ✅
- Sinal enviado: ✅ (HTTP 200)
- Ticket: 123456

Client Copier:
- Sinal recebido: ✅
- Ordem executada: ✅
- Ticket follower: 789012

Pode escalar para dev backend para verificar:
- Persistência no banco de dados
- Broadcast via WebSocket para múltiplos clientes
- Performance da API
```

### Se Houver Problema:
```
❌ PROBLEMA IDENTIFICADO NOS APPS PYTHON

Componente: [Master/Client]
Erro: [Descrição do erro]
Log: [Trecho do log com erro]

Ação: Corrigir apps Python antes de escalar
```

---

## 🚀 Próximos Passos

1. **Iniciar apps** (Master, Client, API)
2. **Verificar conexões** (MT5 + WebSocket)
3. **Abrir ordem no Master**
4. **Observar logs em tempo real**
5. **Preencher checklist**
6. **Gerar reporte**

---

**Pronto para teste!** Aguardando ordem manual no Master MT5.
