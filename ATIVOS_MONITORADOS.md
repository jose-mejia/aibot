# 📊 Sistema de Ativos Monitorados

## 🎯 Funcionalidades Implementadas

### ✅ Backend

1. **Gerenciamento de Ativos**
   - Lista configurável de até 5 ativos
   - Status ativo/inativo por ativo
   - Timeframes configuráveis (inicialmente H1)
   - Persistência em JSON

2. **Coleta de Velas**
   - Coleta automática apenas de velas fechadas
   - Controle de timestamp para evitar duplicação
   - Validação: `agora >= último_timestamp + timeframe`
   - Coleta manual via endpoint

3. **Armazenamento Local**
   - Estrutura: `data/market_data/{SYMBOL}/{TIMEFRAME}.json`
   - Um arquivo por ativo/timeframe
   - Dados persistentes em JSON
   - Histórico completo de velas

### ✅ Frontend

1. **Painel de Ativos**
   - Nova aba "📊 Ativos" no dashboard
   - Lista de até 5 ativos configuráveis
   - Toggle ativo/inativo
   - Seleção de timeframes
   - Botão de coleta manual
   - Estatísticas de coleta

2. **Ativos Padrão**
   - EURUSD ✅
   - GBPUSD ✅
   - USDJPY ✅
   - USDCHF ✅
   - BTCUSD ✅
   - Todos iniciam como ativos com H1

## 📁 Estrutura de Dados

### Arquivos Criados

```
/data
  /market_data
    /EURUSD
      H1.json
    /GBPUSD
      H1.json
    /USDJPY
      H1.json
    /USDCHF
      H1.json
    /BTCUSD
      H1.json
  monitored_assets.json
```

### Formato de Vela

```json
{
  "timestamp": "2024-12-20T18:00:00+00:00",
  "open": 1.0850,
  "high": 1.0860,
  "low": 1.0845,
  "close": 1.0855,
  "volume": 1234
}
```

## 🔌 Endpoints da API

### GET /api/assets
Retorna lista de ativos monitorados

### POST /api/assets
Atualiza lista de ativos monitorados
```json
[
  {
    "symbol": "EURUSD",
    "active": true,
    "timeframes": ["H1"]
  }
]
```

### POST /api/assets/collect
Coleta velas de todos os ativos ativos

### GET /api/assets/{symbol}/candles
Retorna velas de um ativo específico
- Parâmetros: `timeframe` (default: H1), `limit` (default: 100)

## 🔄 Fluxo de Coleta

1. **Bot Ligado:**
   - Loop principal verifica ativos ativos
   - Para cada ativo/timeframe:
     - Verifica se deve coletar (timestamp)
     - Coleta apenas última vela fechada
     - Salva em JSON

2. **Coleta Manual:**
   - Usuário clica "COLETAR VELAS AGORA"
   - Sistema coleta de todos os ativos ativos
   - Retorna estatísticas

3. **Validação de Timestamp:**
   ```
   Se última vela foi coletada às 18:00 (H1)
   Próxima coleta só após 19:00
   Evita duplicação e sobrecarga
   ```

## 🧠 Uso pela IA

Os dados coletados são salvos como "memória" da IA:

- **Análise Técnica:** IA pode usar histórico completo
- **Treinamento Futuro:** Dados prontos para ML
- **Tomada de Decisão:** Base histórica para análise
- **Backtest:** Dados históricos para testar estratégias

## 📝 Exemplo de Uso

### 1. Configurar Ativos

1. Acesse aba "📊 Ativos"
2. Configure até 5 ativos
3. Ative/desative conforme necessário
4. Selecione timeframes (H1 inicialmente)
5. Clique "SALVAR CONFIGURAÇÃO"

### 2. Coletar Velas

**Automático:**
- Bot ligado coleta automaticamente
- Apenas velas fechadas são coletadas
- Respeita intervalo de timeframe

**Manual:**
- Clique "COLETAR VELAS AGORA"
- Sistema coleta de todos os ativos ativos
- Veja estatísticas na tela

### 3. Verificar Dados

Dados são salvos em:
```
data/market_data/{SYMBOL}/{TIMEFRAME}.json
```

Cada arquivo contém array de velas ordenadas por timestamp.

## 🔒 Regras de Segurança

- ✅ Máximo de 5 ativos
- ✅ Apenas velas fechadas são coletadas
- ✅ Validação de timestamp evita duplicação
- ✅ Símbolos únicos (sem duplicação)
- ✅ Validação antes de salvar

## 🚀 Próximos Passos

1. **Expansão de Timeframes:**
   - Adicionar M15, M30, H4, D1
   - Interface para seleção múltipla

2. **Visualização de Dados:**
   - Gráficos de velas
   - Estatísticas por ativo
   - Histórico visual

3. **Integração com IA:**
   - IA usa dados históricos para análise
   - Treinamento com dados coletados
   - Análise multi-ativo

## 📚 Arquivos Criados/Modificados

### Backend
- `backend/models/schemas.py` - Modelos de ativos
- `backend/services/asset_service.py` - Gerenciamento de ativos
- `backend/services/candle_collector.py` - Coleta de velas
- `backend/api/routes.py` - Endpoints de ativos
- `backend/services/bot_service.py` - Integração no loop

### Frontend
- `frontend/src/components/AssetsPanel.tsx` - Componente de ativos
- `frontend/src/components/AssetsPanel.css` - Estilos
- `frontend/src/components/Dashboard.tsx` - Integração
- `frontend/src/services/api.ts` - Métodos de API

## ✅ Checklist de Funcionalidades

- [x] Lista configurável de até 5 ativos
- [x] Status ativo/inativo
- [x] Timeframes configuráveis (H1)
- [x] Ativos padrão pré-carregados
- [x] Coleta apenas de velas fechadas
- [x] Controle de timestamp
- [x] Armazenamento local em JSON
- [x] Estrutura por ativo/timeframe
- [x] Interface web completa
- [x] Coleta manual e automática
- [x] Integração no loop do bot

