# 🚀 Guia de Instalação e Configuração

## Pré-requisitos

1. **Python 3.8+** instalado
2. **Node.js 16+** e npm instalados
3. **MetaTrader 5** instalado e configurado
4. **Conta DEMO** no MetaTrader 5 (obrigatório)

## 📦 Instalação

### 1. Backend (Python)

```bash
# Navegar para o diretório backend
cd backend

# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Frontend (React)

```bash
# Navegar para o diretório frontend
cd frontend

# Instalar dependências
npm install
```

## ⚙️ Configuração

### MetaTrader 5

1. Abra o MetaTrader 5
2. Faça login em uma conta **DEMO**
3. Certifique-se de que o **Trading Automatizado** está habilitado:
   - Menu: `Ferramentas` → `Opções` → `Expert Advisors`
   - Marque "Permitir trading automatizado"
   - Marque "Permitir importação de DLL"

## 🎯 Execução

### 1. Iniciar Backend

```bash
cd backend
python main.py
```

O backend estará disponível em: `http://localhost:8000`

### 2. Iniciar Frontend

Em outro terminal:

```bash
cd frontend
npm start
```

O frontend abrirá automaticamente em: `http://localhost:3000`

## 📋 Primeiros Passos

1. **Abrir o Frontend**: Acesse `http://localhost:3000`

2. **Testar Conexão MT5**: 
   - Vá para a aba "Controle"
   - Clique em "TESTAR CONEXÃO MT5"
   - Verifique se a conexão foi bem-sucedida

3. **Configurar o Bot**:
   - Vá para a aba "Configurações"
   - Ajuste os parâmetros conforme necessário
   - Clique em "SALVAR CONFIGURAÇÕES"

4. **Iniciar o Bot**:
   - Volte para a aba "Controle"
   - Clique em "LIGAR BOT"
   - O bot começará a analisar o mercado e executar trades

5. **Monitorar**:
   - Use a aba "Operações" para ver trades
   - Use a aba "Logs" para ver logs do sistema

## 🔒 Segurança

- ⚠️ **IMPORTANTE**: O sistema está configurado para operar **APENAS em conta DEMO**
- O sistema não executará trades se detectar que não está em conta DEMO
- Sempre teste em conta DEMO antes de qualquer uso em produção
- Stop Loss e Take Profit são obrigatórios

## 🐛 Solução de Problemas

### Erro: "MT5 não está conectado"

- Verifique se o MetaTrader 5 está aberto
- Verifique se você está logado em uma conta DEMO
- Tente clicar em "TESTAR CONEXÃO MT5" novamente

### Erro: "Falha ao inicializar MT5"

- Verifique se o MetaTrader 5 está instalado corretamente
- Verifique se o caminho do MT5 está acessível
- Tente reiniciar o MetaTrader 5

### Frontend não conecta ao Backend

- Verifique se o backend está rodando em `http://localhost:8000`
- Verifique se não há erros no console do backend
- Verifique o arquivo `frontend/src/services/api.ts` se a URL está correta

## 📚 Documentação da API

A documentação interativa da API está disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 💾 Armazenamento

Os dados são armazenados localmente em:
- Banco de dados SQLite: `data/trading_bot.db`
- Decisões da IA, trades e configurações são salvos automaticamente

## 🎓 Próximos Passos

1. Monitore os trades e logs para entender o comportamento da IA
2. Ajuste as configurações conforme necessário
3. Os dados de aprendizado são salvos automaticamente no banco de dados
4. Futuramente, esses dados podem ser usados para treinar modelos de ML
