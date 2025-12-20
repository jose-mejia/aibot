# 🚀 Passo a Passo: Como Rodar o AI Trading Bot

## 📋 Pré-requisitos Verificados

Antes de começar, certifique-se de ter:
- ✅ Python instalado (3.8+)
- ✅ **Node.js instalado (16+)** - Se não tiver, veja [INSTALAR_NODEJS.md](INSTALAR_NODEJS.md)
- ✅ MetaTrader 5 instalado e aberto
- ✅ Conta DEMO logada no MT5
- ✅ Trading Automatizado habilitado no MT5

### ⚠️ Não tem Node.js?

**Instale agora:**
1. Baixe de: https://nodejs.org/ (versão LTS)
2. Instale marcando "Add to PATH"
3. Verifique: `node --version` e `npm --version`
4. Veja guia completo em: [INSTALAR_NODEJS.md](INSTALAR_NODEJS.md)

---

## 🔧 PASSO 1: Preparar o Backend

### 1.1 Abrir Terminal/PowerShell

Abra um terminal na pasta do projeto:
```bash
cd C:\Users\josemejia\dev\python\aibot
```

### 1.2 Navegar para Backend

```bash
cd backend
```

### 1.3 Criar/Ativar Ambiente Virtual

**Se ainda não criou o ambiente virtual:**
```bash
python -m venv venv
```

**Ativar ambiente virtual:**

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

**✅ Sucesso:** Você verá `(venv)` no início da linha do terminal

### 1.4 Atualizar pip

```bash
python -m pip install --upgrade pip
```

### 1.5 Instalar Dependências

```bash
# Instalar MetaTrader5 primeiro (pode dar problema se instalar tudo junto)
pip install MetaTrader5

# Depois instalar todas as outras dependências
pip install -r requirements.txt
```

**⏱️ Tempo:** 2-5 minutos

**✅ Verificar instalação:**
```bash
pip list
# Deve mostrar todas as bibliotecas instaladas
```

---

## 🎨 PASSO 2: Preparar o Frontend

### 2.1 Abrir NOVO Terminal

**Importante:** Mantenha o terminal do backend aberto e ative um NOVO terminal

### 2.2 Navegar para Frontend

```bash
cd C:\Users\josemejia\dev\python\aibot\frontend
```

### 2.3 Instalar Dependências do Frontend

**⚠️ IMPORTANTE:** Você DEVE instalar as dependências antes de rodar!

```bash
npm install
```

**⏱️ Tempo:** 2-5 minutos (primeira vez pode demorar mais)

**✅ Você verá algo como:**
```
added 1500+ packages, and audited 1501 packages in 2m
```

**✅ Verificar se instalou:**
```bash
# Verificar se pasta node_modules existe
dir node_modules

# Ou verificar lista de pacotes
npm list --depth=0
```

**❌ Se der erro "react-scripts não é reconhecido":**
- Significa que `npm install` não foi executado ou falhou
- Veja solução completa em: [SOLUCAO_REACT_SCRIPTS.md](SOLUCAO_REACT_SCRIPTS.md)

---

## ⚙️ PASSO 3: Configurar MetaTrader 5

### 3.1 Abrir MetaTrader 5

- Abra o aplicativo MetaTrader 5

### 3.2 Fazer Login em Conta DEMO

- Faça login em uma conta **DEMO** (não conta real!)
- Se não tiver conta DEMO, crie uma no seu broker

### 3.3 Habilitar Trading Automatizado

1. No MT5, vá em: `Ferramentas` → `Opções`
2. Clique na aba `Expert Advisors`
3. Marque as opções:
   - ✅ **Permitir trading automatizado**
   - ✅ **Permitir importação de DLL**
4. Clique em `OK`

**⚠️ IMPORTANTE:** O bot só funciona em conta DEMO!

---

## 🚀 PASSO 4: Iniciar o Backend

### 4.1 No Terminal do Backend

**Certifique-se de que:**
- Está na pasta `backend`
- Ambiente virtual está ativado (veja `(venv)` no terminal)

### 4.2 Executar Backend

```bash
python main.py
```

### 4.3 Verificar se Iniciou Corretamente

**✅ Sucesso quando ver:**
```
🚀 Iniciando AI Trading Bot Backend...
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**🌐 Backend rodando em:** `http://localhost:8000`

**📚 Documentação da API:** `http://localhost:8000/docs`

**⚠️ NÃO FECHE ESTE TERMINAL!** Deixe rodando.

---

## 🎨 PASSO 5: Iniciar o Frontend

### 5.1 No Terminal do Frontend

**Certifique-se de que:**
- Está na pasta `frontend`
- Dependências foram instaladas

### 5.2 Executar Frontend

```bash
npm start
```

### 5.3 Verificar se Iniciou Corretamente

**✅ Sucesso quando ver:**
```
Compiled successfully!

You can now view ai-trading-bot-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**🌐 O navegador abrirá automaticamente** em `http://localhost:3000`

**⚠️ NÃO FECHE ESTE TERMINAL!** Deixe rodando.

---

## 🎮 PASSO 6: Usar o Sistema

### 6.1 Acessar Interface

- O navegador deve abrir automaticamente em `http://localhost:3000`
- Se não abrir, acesse manualmente: `http://localhost:3000`

### 6.2 Testar Conexão MT5

1. Na interface, vá para a aba **"Controle"**
2. Clique no botão **"🔌 TESTAR CONEXÃO MT5"**
3. Deve aparecer uma mensagem de sucesso com:
   - ✅ Status: Conectado
   - Informações da conta (login, servidor, saldo)

**Se der erro:**
- Verifique se o MT5 está aberto
- Verifique se está logado em conta DEMO
- Verifique se Trading Automatizado está habilitado

### 6.3 Configurar o Bot

1. Vá para a aba **"⚙️ Configurações"**
2. Ajuste os parâmetros:
   - **Timeframe:** M15 (recomendado para início)
   - **Volume:** 0.01 (mínimo, seguro para testes)
   - **Stop Loss:** 50 pontos
   - **Take Profit:** 100 pontos
   - **Intervalo de Análise:** 60 segundos
   - **Máximo de Trades Simultâneos:** 1
3. Clique em **"💾 SALVAR CONFIGURAÇÕES"**
4. Deve aparecer mensagem de sucesso

### 6.4 Iniciar o Bot

1. Volte para a aba **"🎮 Controle"**
2. Verifique se mostra:
   - **Status do Bot:** 🔴 Parado
   - **Conexão MT5:** 🟢 Conectado
3. Clique no botão **"▶️ LIGAR BOT"**
4. O status deve mudar para **🟢 Executando**

### 6.5 Monitorar o Bot

**Aba "📈 Operações":**
- Veja trades executados
- Estatísticas de lucro/prejuízo
- Status das operações (aberta/fechada)

**Aba "📝 Logs":**
- Veja decisões da IA em tempo real
- Logs do sistema
- Erros e avisos

---

## 🛑 Como Parar o Sistema

### Parar o Bot (sem fechar servidores)

1. Na interface, aba **"Controle"**
2. Clique em **"⏹️ DESLIGAR BOT"**

### Parar Backend

No terminal do backend:
```
Ctrl + C
```

### Parar Frontend

No terminal do frontend:
```
Ctrl + C
```

---

## 🔄 Resumo Rápido (Comandos)

### Terminal 1 - Backend
```bash
cd backend
venv\Scripts\activate  # Windows (se não estiver ativado)
python main.py
```

### Terminal 2 - Frontend
```bash
cd frontend
npm start
```

### Depois
1. Acesse: `http://localhost:3000`
2. Teste conexão MT5
3. Configure parâmetros
4. Ligue o bot

---

## ✅ Checklist de Execução

- [ ] Backend rodando (terminal 1)
- [ ] Frontend rodando (terminal 2)
- [ ] Navegador aberto em `http://localhost:3000`
- [ ] MT5 aberto e logado em conta DEMO
- [ ] Trading Automatizado habilitado no MT5
- [ ] Conexão MT5 testada com sucesso
- [ ] Configurações salvas
- [ ] Bot ligado e executando

---

## 🐛 Problemas Comuns

### Backend não inicia

**Erro:** `ModuleNotFoundError`
**Solução:**
```bash
# Certifique-se de que ambiente virtual está ativado
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Frontend não conecta ao Backend

**Erro:** `Network Error` ou `Cannot connect`
**Solução:**
- Verifique se backend está rodando em `http://localhost:8000`
- Acesse `http://localhost:8000/docs` para verificar
- Verifique se não há firewall bloqueando

### MT5 não conecta

**Erro:** "MT5 não está conectado"
**Solução:**
- Verifique se MT5 está aberto
- Verifique se está logado em conta DEMO
- Verifique se Trading Automatizado está habilitado
- Reinicie o MT5 e tente novamente

### Porta já em uso

**Erro:** `Address already in use`
**Solução:**
- Feche outros programas usando a porta
- Ou altere a porta no código

---

## 📞 Próximos Passos

1. **Monitore os trades** na aba "Operações"
2. **Analise os logs** para entender decisões da IA
3. **Ajuste configurações** conforme necessário
4. **Os dados são salvos automaticamente** em `data/trading_bot.db`

---

## 🎉 Pronto!

Se seguiu todos os passos, seu bot de trading está rodando!

**Lembre-se:**
- ⚠️ Use apenas conta DEMO
- 📊 Monitore regularmente
- 🔒 Stop Loss e Take Profit são obrigatórios
- 📝 Logs mostram todas as decisões da IA

