# ✅ Checklist de QA & Testes (Quality Assurance)

Roteiro para validar a estabilidade do sistema antes de uma Release.

---

## 1. Testes de Ambiente
- [ ] **API Server:** Iniciado sem erros e conectado ao `aibot.db`.
- [ ] **MT5 Master:** Aberto na conta correta (`7409735`). Algo Trading Habilitado.
- [ ] **MT5 Client:** Aberto na conta correta (`11629107`). Algo Trading Habilitado.

## 2. Testes de Interface e Login
- [ ] **Master Sender:** 
  - Login com sucesso (`master`).
  - Dashboard carrega.
  - Log mostra `Connected to MT5: 7409735`.
- [ ] **Client Copier:** 
  - Login com sucesso (`client`).
  - Dashboard carrega.
  - Log mostra `Connected to MT5: 11629107`.

## 3. Teste de Fluxo de Ordens (End-to-End)

### Cenário A: Ordem a Mercado (BUY/SELL)
1.  No MT5 Master, abrir uma ordem de **Compra (BUY) 0.01 em EURUSD**.
2.  Verificar no Log do Master: `Signal Detected: BUY EURUSD`.
3.  Verificar no Log do Client: `Signal Received` -> `Order Executed`.
4.  Confirmar no MT5 Client se a ordem foi aberta com sucesso.
5.  Repetir para **Venda (SELL)**.

### Cenário B: Ordens Pendentes (LIMIT/STOP)
1.  No MT5 Master, colocar um **Buy Limit** 100 pontos abaixo do preço.
2.  Verificar se o Client replicou a ordem pendente.

### Cenário C: Modificação (SL/TP)
1.  Na ordem aberta no Master, adicionar ou mudar o **Stop Loss**.
2.  Verificar se o Client atualizou o SL da ordem correspondente (via Ticket Map).

### Cenário D: Fechamento (Close)
1.  Fechar a ordem no Master.
2.  Verificar se o Client fechou a ordem imediatamente.

## 4. Testes de Robustez
- [ ] **Reconexão:** Feche o MT5 Client e reabra. O Copier deve reconectar e sincronizar? (Atualmente ele só reconecta se reiniciar o App).
- [ ] **Volume Inválido:** Tente abrir 0.001 no Master (se o Client só aceitar 0.01). O Client deve arredondar para o mínimo ou rejeitar (ver logs de erro).
