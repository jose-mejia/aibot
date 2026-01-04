# 🚀 AIBOT Trade Copier - Guia Rápido de Início

## ⚡ Início Rápido (3 Passos)

### 1️⃣ Compilar os Executáveis
```bash
build_test_exe.bat
```
Aguarde a compilação terminar (~5-10 minutos na primeira vez)

### 2️⃣ Configurar as Contas MT5
Edite os arquivos em `dist_test/`:

**config_sender.json** (Conta Master)
```json
{
  "mt5": {
    "login": SEU_LOGIN_MASTER,
    "password": "SUA_SENHA_MASTER",
    "server": "SEU_SERVIDOR"
  }
}
```

**config_client.json** (Conta Client)
```json
{
  "mt5": {
    "login": SEU_LOGIN_CLIENT,
    "password": "SUA_SENHA_CLIENT",
    "server": "SEU_SERVIDOR"
  }
}
```

### 3️⃣ Testar
```bash
quick_test.bat
```

Isso abrirá 3 janelas:
- ✅ API Server (Rust)
- ✅ Master Sender (Python)
- ✅ Client Copier (Python)

---

## 📋 Pré-requisitos

- ✅ Windows 10/11
- ✅ Python 3.8+ instalado
- ✅ Rust instalado (para compilar API server)
- ✅ MetaTrader 5 instalado
- ✅ 2 contas MT5 (Master e Client)

---

## 🎯 Teste Básico

1. **Abra o MT5** e faça login na conta Master
2. **Execute** `quick_test.bat`
3. **Aguarde** todos os serviços iniciarem (~15 segundos)
4. **Abra uma ordem** no MT5 Master (ex: BUY 0.01 EURUSD)
5. **Verifique** se a ordem aparece no MT5 Client

---

## 📁 Estrutura de Arquivos

```
aibot/backend/copy/
│
├── api_server/              # Servidor Rust (porta 8000)
│   ├── src/
│   └── Cargo.toml
│
├── master_sender/           # Monitor da conta Master
│   ├── main_sender.py
│   ├── sender_service.py
│   └── config_sender.json
│
├── client_copier/           # Copiador para conta Client
│   ├── main_client.py
│   ├── client_service.py
│   └── config_client.json
│
├── dist_test/               # Executáveis compilados
│   ├── api_server.exe
│   ├── master_sender.exe
│   ├── client_copier.exe
│   ├── config_sender.json
│   └── config_client.json
│
└── Scripts úteis:
    ├── build_test_exe.bat   # Compila tudo
    ├── quick_test.bat       # Inicia todos os serviços
    └── clean_build.bat      # Limpa builds anteriores
```

---

## 🔧 Configurações Avançadas

### Modo de Cópia de Volume

Em `config_client.json`:

**Modo Fixo** (sempre copia com volume fixo):
```json
"trade_copy": {
  "mode": "fix",
  "fixed_lot": 0.01
}
```

**Modo Multiplicador** (multiplica o volume do Master):
```json
"trade_copy": {
  "mode": "multiplier",
  "multiplier": 0.5  // Copia com 50% do volume
}
```

### Safety Rules

Proteções automáticas em `config_client.json`:
```json
"trade_copy": {
  "max_slippage_points": 50,    // Máx slippage permitido
  "max_spread_points": 20,       // Máx spread permitido
  "max_exposure_trades": 5,      // Máx ordens simultâneas
  "max_exposure_lots": 10.0      // Máx volume total
},
"safety": {
  "max_drawdown_percent": 10     // Para se drawdown > 10%
}
```

---

## 📊 Monitoramento

### Logs em Tempo Real

**Master Sender:**
```bash
tail -f dist_test/sender.log
```

**Client Copier:**
```bash
tail -f dist_test/client.log
```

**API Server:**
Veja a janela do console do API Server

### O que Observar

✅ **Master Sender detectou ordem:**
```
INFO - Order detected: Ticket=123456, Symbol=EURUSD, Type=BUY
INFO - Sending signal to API...
INFO - Signal sent successfully
```

✅ **Client Copier recebeu e copiou:**
```
INFO - WebSocket message received
INFO - Processing signal: EURUSD BUY 0.01
INFO - Order copied: Ticket=789012
```

---

## 🐛 Troubleshooting Rápido

### ❌ "Failed to connect to MT5"
- Certifique-se que o MT5 está aberto e logado
- Verifique se as credenciais estão corretas
- Tente reiniciar o MT5

### ❌ "Connection refused to API"
- Verifique se o API Server está rodando
- Verifique se a porta 8000 está livre
- Tente: `netstat -ano | findstr :8000`

### ❌ "WebSocket connection failed"
- Certifique-se que o API Server iniciou completamente
- Verifique o log do API Server
- Tente reiniciar o Client Copier

### ❌ "Order not copied"
- Verifique os safety rules (spread, slippage)
- Verifique se há margem suficiente
- Verifique se o símbolo está disponível no Client
- Veja o client.log para detalhes

### 🔄 Rebuild Limpo
Se algo não funcionar:
```bash
clean_build.bat
build_test_exe.bat
```

---

## 📚 Documentação Adicional

- **ARCHITECTURE.md** - Diagrama completo da arquitetura
- **TESTING_GUIDE.md** - Guia detalhado de testes
- **dist_test/README.txt** - Instruções na pasta de distribuição

---

## 🎓 Próximos Passos

Após validar o funcionamento básico:

1. **Teste com múltiplos clientes** - Execute vários `client_copier.exe`
2. **Teste de reconexão** - Pare e reinicie componentes
3. **Teste de stress** - Abra múltiplas ordens rapidamente
4. **Build de produção** - Use `build_release.bat` com GUI Tauri
5. **Deploy em servidor** - Configure o API server em VPS

---

## 💡 Dicas

- 🔐 **Nunca commite** arquivos de configuração com senhas reais
- 📝 **Sempre verifique os logs** antes de reportar problemas
- 🧪 **Teste em conta demo** antes de usar em conta real
- 💾 **Faça backup** das configurações antes de atualizar
- 🔄 **Use clean_build.bat** se tiver problemas de compilação

---

## 🆘 Suporte

Se precisar de ajuda:
1. Verifique os logs (sender.log, client.log)
2. Leia TESTING_GUIDE.md
3. Revise ARCHITECTURE.md
4. Tente um rebuild limpo

---

**Boa sorte com seu Trade Copier! 🚀📈**
