# 📊 Fluxo: Fechamento de Ordem (CLOSE)

**Tipo:** Fluxo Principal  
**Versão:** 1.0  
**Data:** 2026-01-04

---

## 🎯 Objetivo

Fechar automaticamente ordens no Client quando fechadas no Master.

---

## 🔄 Fluxo Simplificado

```
Master: Fecha ordem
    ↓
Master Sender: Detecta ausência
    ↓
API: Envia CLOSE signal
    ↓
Client: Recebe CLOSE
    ↓
Client: Fecha ordem local
```

---

## 📝 Detalhamento

### 1. Detecção de Fechamento
**Código:** `master_sender/sender_service.py` linha 168-171

```python
closed_tickets = [t for t in self.last_state if t not in current_map]
for t in closed_tickets:
    logger.info(f"Trade Closed/Removed on Master: {t}")
    self._send_close(t)
    del self.last_state[t]
```

---

### 2. Envio do Sinal
**Endpoint:** `POST /signals/close`  
**Payload:**
```json
{
    "master_ticket": 12345
}
```

---

### 3. Fechamento no Client
**Função:** `close_trade()` (client_service.py linha 303)

```python
record = self.db.get_trade(master_ticket, self.config['mt5']['login'])
if record and record['status'] == 'OPEN':
    # Busca posição local
    for p in mt5.positions_get():
        if p.comment == f"COPY_{master_ticket}":
            # Fecha posição
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": p.ticket,
                "volume": p.volume,
                "type": mt5.ORDER_TYPE_SELL if p.type == 0 else mt5.ORDER_TYPE_BUY
            }
            mt5.order_send(request)
```

---

## ✅ Checklist de Teste

- [ ] Fechar ordem manualmente no Master
- [ ] Verificar log "Trade Closed/Removed"
- [ ] Verificar log "Close Signal"
- [ ] Confirmar fechamento no Client
- [ ] Verificar status no banco = 'CLOSED'

---

**Documentos Relacionados:**
- [Fluxo de Abertura](FLOW_OPEN_ORDER.md)
- [Fluxo de Modificação](FLOW_MODIFY.md)
