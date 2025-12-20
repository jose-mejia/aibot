# 🤖 AI Trading Bot - MVP

Sistema de Trading Automatizado com Inteligência Artificial integrado ao MetaTrader 5.

## 📋 Características

- ✅ Conecta ao MetaTrader 5 localmente
- ✅ Core de IA desacoplado e modular
- ✅ Interface web em tempo real (React + TypeScript)
- ✅ Controle completo (ligar/desligar, configurar)
- ✅ Operação apenas em conta DEMO
- ✅ Armazenamento local (SQLite) para aprendizado
- ✅ Código limpo e modular

## 🏗️ Arquitetura

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

## 📁 Estrutura do Projeto

```
/backend
  /api              # Endpoints REST
  /core_ai          # Core de IA (desacoplado)
  /mt5              # Integração MT5
  /services         # Serviços principais
  /storage          # Armazenamento local
  /models           # Modelos de dados
  main.py

/frontend
  /components       # Componentes React
  /pages            # Páginas
  /services         # Serviços de API
  App.tsx
```

## 🚀 Instalação

### Backend

```bash
cd backend
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## ⚙️ Configuração

1. Instale o MetaTrader 5
2. Configure uma conta DEMO
3. Ative o Trading Automatizado nas configurações do MT5

## 🎯 Uso

### Iniciar Backend

```bash
cd backend
python main.py
```

Backend rodará em: `http://localhost:8000`

### Iniciar Frontend

```bash
cd frontend
npm start
```

Frontend rodará em: `http://localhost:3000`

## 📊 Funcionalidades

- **Controle do Bot**: Ligar/Desligar
- **Configurações**: Par, Timeframe, Volume, SL, TP, Magic Number
- **Operações**: Histórico de trades em tempo real
- **Logs**: Sistema de logs detalhado
- **IA**: Decisões da IA registradas para aprendizado

## 🔒 Segurança

- Operação apenas em conta DEMO
- Kill switch imediato
- Apenas 1 trade ativo por par (configurável)
- Validação de SL e TP obrigatórios
- Logs detalhados de erro

## 📝 Licença

Proprietário - Uso interno
