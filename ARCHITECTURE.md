# 🏗️ Arquitetura do Sistema

## Visão Geral

O sistema segue uma arquitetura modular e desacoplada, permitindo evolução independente de cada componente.

```
[ Interface Web (React + TypeScript) ]
               ↓ REST API
[ Backend Local (FastAPI - Python) ]
               ↓
[ Core de IA (Python - Modular) ]
               ↓
[ Gerenciador MT5 (MetaTrader 5 Local) ]
               ↓
[ Armazenamento Local (SQLite) ]
```

## 📁 Estrutura de Módulos

### Backend

```
/backend
  /api              # Endpoints REST (camada de apresentação)
    routes.py        # Rotas da API
  /core_ai          # Core de IA (desacoplado)
    ai_engine.py    # Motor de análise e decisão
  /mt5              # Integração MT5
    connector.py    # Conexão com MT5
    trade_manager.py # Gerenciamento de operações
  /services         # Serviços principais
    bot_service.py  # Orquestrador principal
  /storage          # Armazenamento local
    database.py     # Gerenciador SQLite
  /models           # Modelos de dados
    schemas.py      # Schemas Pydantic
  main.py           # Aplicação FastAPI
```

### Frontend

```
/frontend
  /components       # Componentes React
    Dashboard.tsx   # Dashboard principal
    ControlPanel.tsx # Controle do bot
    ConfigPanel.tsx # Configurações
    OperationsPanel.tsx # Operações
    LogsPanel.tsx  # Logs
  /services         # Serviços de API
    api.ts         # Cliente HTTP
  App.tsx          # Componente raiz
```

## 🔄 Fluxo de Dados

### 1. Inicialização

1. Usuário acessa interface web
2. Frontend faz requisição `GET /api/status`
3. Backend retorna status do sistema

### 2. Configuração

1. Usuário ajusta configurações no frontend
2. Frontend envia `POST /api/config`
3. Backend valida e salva configurações
4. Configurações são persistidas no SQLite

### 3. Início do Bot

1. Usuário clica em "LIGAR BOT"
2. Frontend envia `POST /api/bot/start`
3. Backend valida conexão MT5
4. Backend inicia thread de execução
5. Loop principal começa

### 4. Loop de Execução

```
1. Verificar conexão MT5
2. Verificar limite de trades simultâneos
3. Coletar candles do MT5
4. Enviar dados para Core de IA
5. Core de IA analisa e retorna decisão
6. Salvar decisão no banco de dados
7. Se decisão != HOLD:
   - Validar regras de segurança
   - Executar trade via Trade Manager
   - Salvar trade no banco de dados
8. Aguardar intervalo de análise
9. Repetir
```

### 5. Monitoramento

1. Frontend faz polling a cada 3 segundos
2. Busca trades: `GET /api/trades`
3. Busca logs: `GET /api/logs`
4. Atualiza interface em tempo real

## 🧠 Core de IA

### Responsabilidades

- **Receber dados**: Candles do mercado
- **Calcular indicadores**: RSI, Médias Móveis, MACD
- **Tomar decisões**: Baseado em regras (Fase 1)
- **Retornar decisões**: Estruturadas (action, confidence, reason)

### Não Faz

- ❌ Não executa ordens
- ❌ Não gerencia trades
- ❌ Não acessa MT5 diretamente

### Estrutura de Decisão

```python
{
  "action": "BUY | SELL | HOLD",
  "confidence": 0.0-1.0,
  "reason": "string explicando o motivo",
  "timestamp": "datetime",
  "indicators": {
    "rsi": 45.2,
    "ma_fast": 1.0850,
    "ma_slow": 1.0840,
    ...
  }
}
```

## 🔌 Integração MT5

### MT5Connector

- Gerencia conexão com MT5
- Obtém candles históricos
- Obtém preços atuais
- Valida conta DEMO

### TradeManager

- Abre ordens no MT5
- Gerencia posições abertas
- Fecha posições
- Aplica regras de risco
- Valida SL e TP obrigatórios

## 💾 Armazenamento

### SQLite Database

**Tabelas:**

1. **ai_decisions**: Decisões da IA
   - timestamp, action, confidence, reason, indicators

2. **trades**: Trades executados
   - id, symbol, type, entry_price, exit_price, profit, status

3. **candles**: Histórico de candles (preparado para futuro)

4. **config**: Configurações do sistema

### Uso Futuro

- Dados para treinamento de ML
- Backtest de estratégias
- Análise de performance
- Otimização de parâmetros

## 🔒 Segurança

### Validações Implementadas

1. **Conta DEMO obrigatória**
2. **Stop Loss e Take Profit obrigatórios**
3. **Limite de trades simultâneos**
4. **Kill switch imediato**
5. **Validação antes de executar ordens**

### Regras de Risco

- Apenas 1 trade ativo por par (configurável)
- SL e TP sempre definidos
- Validação de conexão MT5 antes de operar
- Logs detalhados de todas as operações

## 🚀 Evolução Futura

### Fase 2: Machine Learning

- Treinar modelos com dados históricos
- Substituir regras por modelo treinado
- Otimização contínua

### Fase 3: Reinforcement Learning

- Aprendizado por reforço
- Reward = lucro, Penalty = perda
- Política de decisão adaptativa

### Fase 4: Servidor Central

- Migração para servidor
- Múltiplos usuários
- Dashboard administrativo

### Fase 5: SaaS

- Assinaturas
- Licenciamento
- Múltiplos pares simultâneos

## 📝 Princípios de Design

1. **Separação de Responsabilidades**: Cada módulo tem uma responsabilidade clara
2. **Desacoplamento**: Core de IA não depende de MT5 ou storage
3. **Modularidade**: Fácil adicionar/remover módulos
4. **Testabilidade**: Cada módulo pode ser testado independentemente
5. **Escalabilidade**: Preparado para crescimento futuro

