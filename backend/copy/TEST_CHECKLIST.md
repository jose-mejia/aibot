# ✅ Checklist de Teste - AIBOT Trade Copier

## 📋 Pré-Requisitos

- [ ] Python 3.8+ instalado e no PATH
- [ ] Rust instalado (rustc --version funciona)
- [ ] MetaTrader 5 instalado
- [ ] 2 contas MT5 disponíveis (Master e Client)
- [ ] Contas MT5 permitem trading automatizado
- [ ] Git instalado (opcional, para versionamento)

---

## 🔨 Build e Compilação

- [ ] Executado `build_test_exe.bat` sem erros
- [ ] Arquivo `dist_test/master_sender.exe` criado
- [ ] Arquivo `dist_test/client_copier.exe` criado
- [ ] Arquivo `dist_test/api_server.exe` criado (ou compilado em api_server/)
- [ ] Arquivos de configuração copiados para `dist_test/`

---

## ⚙️ Configuração

### Master Sender (config_sender.json)
- [ ] `api.url` configurado corretamente (http://127.0.0.1:8000)
- [ ] `api.username` definido
- [ ] `api.password` definido
- [ ] `mt5.login` com número da conta Master
- [ ] `mt5.password` com senha correta
- [ ] `mt5.server` com nome do servidor correto

### Client Copier (config_client.json)
- [ ] `api.url` configurado corretamente (http://127.0.0.1:8000)
- [ ] `api.ws_url` configurado corretamente (ws://127.0.0.1:8000)
- [ ] `api.username` definido
- [ ] `api.password` definido
- [ ] `mt5.login` com número da conta Client
- [ ] `mt5.password` com senha correta
- [ ] `mt5.server` com nome do servidor correto
- [ ] `trade_copy.mode` definido ("fix" ou "multiplier")
- [ ] `trade_copy.fixed_lot` ou `multiplier` configurado
- [ ] Safety rules configuradas adequadamente

---

## 🚀 Teste de Inicialização

### API Server
- [ ] API Server inicia sem erros
- [ ] Porta 8000 está livre
- [ ] Mensagem "Server listening on 0.0.0.0:8000" aparece
- [ ] Endpoint `/health` responde OK
- [ ] Banco de dados SQLite criado

### Master Sender
- [ ] Master Sender conecta ao MT5 Master
- [ ] Mensagem "Connected to MT5" aparece
- [ ] Não há erros de autenticação MT5
- [ ] Master Sender faz login na API
- [ ] Token JWT recebido com sucesso

### Client Copier
- [ ] Client Copier conecta ao MT5 Client
- [ ] Mensagem "Connected to MT5" aparece
- [ ] Não há erros de autenticação MT5
- [ ] Client Copier faz login na API
- [ ] WebSocket conecta com sucesso
- [ ] Mensagem "WebSocket connected" aparece

---

## 🧪 Testes Funcionais

### Teste 1: Ordem BUY Simples
- [ ] Abrir ordem BUY no MT5 Master (ex: EURUSD 0.01)
- [ ] Master Sender detecta a ordem
- [ ] Log mostra "Order detected: Ticket=..."
- [ ] Master Sender envia para API
- [ ] Log mostra "Signal sent successfully"
- [ ] Client Copier recebe via WebSocket
- [ ] Log mostra "WebSocket message received"
- [ ] Client Copier copia a ordem
- [ ] Log mostra "Order copied: Ticket=..."
- [ ] Ordem aparece no MT5 Client
- [ ] Parâmetros corretos (símbolo, tipo, volume, SL, TP)

### Teste 2: Ordem SELL Simples
- [ ] Abrir ordem SELL no MT5 Master (ex: GBPUSD 0.01)
- [ ] Master Sender detecta
- [ ] Sinal enviado para API
- [ ] Client Copier recebe e copia
- [ ] Ordem aparece no MT5 Client com parâmetros corretos

### Teste 3: Modificação de Ordem
- [ ] Modificar SL/TP de ordem existente no Master
- [ ] Master Sender detecta modificação
- [ ] Sinal de modificação enviado
- [ ] Client Copier atualiza ordem correspondente
- [ ] SL/TP atualizados no MT5 Client

### Teste 4: Fechamento de Ordem
- [ ] Fechar ordem no MT5 Master
- [ ] Master Sender detecta fechamento
- [ ] Sinal de fechamento enviado
- [ ] Client Copier fecha ordem correspondente
- [ ] Ordem fechada no MT5 Client

### Teste 5: Múltiplas Ordens
- [ ] Abrir 3 ordens diferentes no Master
- [ ] Todas as 3 ordens detectadas
- [ ] Todas as 3 ordens copiadas
- [ ] Todas aparecem no MT5 Client

---

## 🛡️ Testes de Safety Rules

### Teste 6: Max Spread
- [ ] Configurar `max_spread_points: 5` no config_client.json
- [ ] Tentar copiar ordem em símbolo com spread > 5 points
- [ ] Ordem NÃO deve ser copiada
- [ ] Log deve mostrar "Spread too high, skipping"

### Teste 7: Max Slippage
- [ ] Configurar `max_slippage_points: 10`
- [ ] Simular condição de alto slippage
- [ ] Verificar se ordem é rejeitada ou executada com slippage aceitável

### Teste 8: Max Exposure Trades
- [ ] Configurar `max_exposure_trades: 2`
- [ ] Copiar 2 ordens (deve funcionar)
- [ ] Tentar copiar 3ª ordem
- [ ] 3ª ordem NÃO deve ser copiada
- [ ] Log deve mostrar "Max exposure reached"

### Teste 9: Max Exposure Lots
- [ ] Configurar `max_exposure_lots: 0.05`
- [ ] Copiar ordens até atingir 0.05 lots total
- [ ] Próxima ordem NÃO deve ser copiada
- [ ] Log deve mostrar "Max lot exposure reached"

---

## 🔄 Testes de Reconexão

### Teste 10: Reconexão MT5 Master
- [ ] Desconectar MT5 Master
- [ ] Master Sender detecta desconexão
- [ ] Reconectar MT5 Master
- [ ] Master Sender reconecta automaticamente
- [ ] Sistema volta a funcionar

### Teste 11: Reconexão MT5 Client
- [ ] Desconectar MT5 Client
- [ ] Client Copier detecta desconexão
- [ ] Reconectar MT5 Client
- [ ] Client Copier reconecta automaticamente
- [ ] Sistema volta a funcionar

### Teste 12: Reconexão API Server
- [ ] Parar API Server
- [ ] Master Sender e Client Copier detectam desconexão
- [ ] Reiniciar API Server
- [ ] Master Sender reconecta
- [ ] Client Copier reconecta WebSocket
- [ ] Sistema volta a funcionar

### Teste 13: Reconexão WebSocket
- [ ] Simular perda de conexão WebSocket
- [ ] Client Copier tenta reconectar
- [ ] Reconexão bem-sucedida
- [ ] Ordens voltam a ser copiadas

---

## 📊 Testes de Performance

### Teste 14: Latência
- [ ] Abrir ordem no Master
- [ ] Medir tempo até aparecer no Client
- [ ] Latência < 2 segundos (ideal < 1 segundo)

### Teste 15: Múltiplos Clientes
- [ ] Executar 3 instâncias de Client Copier
- [ ] Abrir ordem no Master
- [ ] Todas as 3 instâncias recebem e copiam
- [ ] Sem erros ou conflitos

### Teste 16: Stress Test
- [ ] Abrir 10 ordens rapidamente no Master
- [ ] Todas as 10 ordens detectadas
- [ ] Todas as 10 ordens copiadas
- [ ] Sem perda de sinais
- [ ] Sem erros de execução

---

## 🔐 Testes de Segurança

### Teste 17: Autenticação
- [ ] Tentar conectar com credenciais inválidas
- [ ] Conexão deve ser rejeitada
- [ ] Mensagem de erro apropriada

### Teste 18: Token Expirado
- [ ] Aguardar token JWT expirar
- [ ] Sistema deve renovar token automaticamente
- [ ] Ou mostrar erro e solicitar novo login

---

## 📝 Testes de Logs

### Teste 19: Logs do Master Sender
- [ ] Arquivo `sender.log` criado
- [ ] Logs contêm timestamps
- [ ] Logs contêm níveis (INFO, ERROR, etc.)
- [ ] Ordens detectadas registradas
- [ ] Sinais enviados registrados
- [ ] Erros registrados com detalhes

### Teste 20: Logs do Client Copier
- [ ] Arquivo `client.log` criado
- [ ] Logs contêm timestamps
- [ ] Sinais recebidos registrados
- [ ] Ordens copiadas registradas
- [ ] Safety rules aplicadas registradas
- [ ] Erros registrados com detalhes

---

## 🎯 Testes de Casos Extremos

### Teste 21: Símbolo Não Disponível
- [ ] Master abre ordem em símbolo não disponível no Client
- [ ] Client Copier detecta símbolo indisponível
- [ ] Ordem NÃO é copiada
- [ ] Log mostra "Symbol not available"

### Teste 22: Margem Insuficiente
- [ ] Client tem margem insuficiente
- [ ] Tentar copiar ordem
- [ ] Ordem NÃO é copiada
- [ ] Log mostra "Insufficient margin"

### Teste 23: Volume Inválido
- [ ] Master abre ordem com volume muito pequeno
- [ ] Client ajusta para volume mínimo permitido
- [ ] Ou rejeita se não puder ajustar
- [ ] Log mostra ajuste ou rejeição

### Teste 24: Mercado Fechado
- [ ] Tentar copiar ordem quando mercado está fechado
- [ ] Ordem NÃO é copiada
- [ ] Log mostra "Market closed"

---

## ✅ Checklist Final

- [ ] Todos os testes funcionais passaram
- [ ] Todos os testes de safety rules passaram
- [ ] Todos os testes de reconexão passaram
- [ ] Performance aceitável (latência < 2s)
- [ ] Logs funcionando corretamente
- [ ] Sem memory leaks (executar por 1 hora)
- [ ] Documentação revisada e atualizada
- [ ] Configurações de exemplo atualizadas
- [ ] README.txt na pasta dist_test atualizado

---

## 📦 Pronto para Produção?

Se todos os itens acima estão marcados:

- [ ] Fazer backup das configurações
- [ ] Testar em conta demo por 24 horas
- [ ] Monitorar logs continuamente
- [ ] Documentar quaisquer problemas encontrados
- [ ] Ajustar safety rules conforme necessário
- [ ] Preparar plano de rollback
- [ ] Definir procedimentos de monitoramento
- [ ] Treinar usuários finais

---

## 🚨 Critérios de Go/No-Go

### ✅ GO (Pode usar em produção)
- Todos os testes críticos (1-13) passaram
- Latência < 2 segundos consistentemente
- Sem crashes em 24h de teste
- Logs claros e informativos
- Safety rules funcionando corretamente

### ❌ NO-GO (NÃO usar em produção)
- Qualquer teste crítico falhou
- Latência > 5 segundos
- Crashes ou memory leaks
- Logs ausentes ou confusos
- Safety rules não funcionam

---

**Data do Teste:** _______________
**Testado por:** _______________
**Versão:** _______________
**Resultado:** ☐ APROVADO  ☐ REPROVADO

**Observações:**
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
