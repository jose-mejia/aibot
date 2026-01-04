# 📊 Fluxo: Modificação de Ordem (MODIFY)

**Tipo:** Fluxo Secundário  
**Versão:** 1.0  
**Data:** 2026-01-04

---

## 🎯 Objetivo

Sincronizar modificações de SL/TP do Master para o Client.

---

## 🔄 Fluxo Simplificado

```
Master: Modifica SL/TP
    ↓
Master Sender: Detecta mudança
    ↓
API: Atualiza sinal
    ↓
Client: Recebe MODIFY
    ↓
Client: Modifica ordem local
```

---

## 📝 Detalhamento

### 1. Detecção de Modificação
**Código:** `master_sender/sender_service.py` linha 157-160

```python
last = self.last_state[ticket]
if abs(p.sl - last['sl']) > 1e-5 or abs(p.tp - last['tp']) > 1e-5:
    logger.info(f"Trade Modified: {ticket} SL/TP Changed")
    self._send_signal(signal_data)
```

**Tolerância:** 0.00001 (1e-5) para evitar falsos positivos

---

### 2. Envio do Sinal
**Endpoint:** `POST /signals/broadcast`  
**Payload:** Idêntico ao OPEN (com SL/TP atualizados)

---

### 3. Processamento no Client
**Função:** `_sync_modifications()` (client_service.py linha 284)

```python
if abs(local.sl - m_item['sl']) > 1e-6 or abs(local.tp - m_item['tp']) > 1e-6:
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "position": local.ticket,
        "sl": round(m_item['sl'], digits),
        "tp": round(m_item['tp'], digits)
    }
    mt5.order_send(request)
```

---

## ✅ Checklist de Teste

- [ ] Modificar SL de ordem existente no Master
- [ ] Verificar log "Trade Modified"
- [ ] Verificar modificação no Client
- [ ] Confirmar SL/TP idênticos

---

**Documentos Relacionados:**
- [Fluxo de Abertura](FLOW_OPEN_ORDER.md)
- [Fluxo de Fechamento](FLOW_CLOSE.md)
