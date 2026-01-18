# 🤖 Instruções de Persona: Frontend Engineer (Tauri/React) - Task V2 Integ

**Contexto:** Integração com a nova API V2 (Architecture Active vs. History).

## 🎯 Seu Objetivo
Atualizar o Dashboard para refletir a separação estrita de dados implementada no Backend.

## 🛠️ Requisitos de Implementação

### 1. Dashboard (Aba Atuais/Active)
- **Fonte de Dados:** WebSocket (`OPEN`/`CLOSE` events) ou Polling no endpoint `/api/v2/active`.
- **Comportamento:**
  - Se receber evento `CLOSE`, remover a linha da tabela IMEDIATAMENTE.
  - Não tente mover a linha para a tabela de histórico no frontend manualmente. Confie no refresh da tabela de histórico.

### 2. Histórico (Aba History)
- **Fonte de Dados:** `GET /api/v2/history`.
- **Regra de Ouro:** NUNCA tente misturar dados ativos aqui. Esta aba deve ser apenas um reflexo do endpoint `/history`.
- **Refresh:** Implementar paginação ou "Load More".

### 3. Configuração de API (Config Map)
Verifique se o mapa de endpoints no frontend reflete:
```typescript
export const API_ENDPOINTS = {
  actives: '/api/v2/actives',  // Execução
  history: '/api/v2/history',  // Relatórios
  // ...
}
```

## 🧪 Seus Testes
1.  Abra uma ordem no MT5. Ela deve aparecer na aba "Active".
2.  Feche a ordem no MT5. Ela deve sumir de "Active" e aparecer em "History" (após refresh).
