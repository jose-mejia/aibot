# 📦 AIBOT Trade Copier - Resumo do Sistema

## 🎯 O que foi criado

Sistema completo de Trade Copier com arquitetura cliente-servidor para copiar ordens entre contas MT5.

---

## 📁 Arquivos Criados

### 🔧 Scripts de Build e Teste

| Arquivo | Descrição |
|---------|-----------|
| `build_test_exe.bat` | **Script principal de build** - Compila API Server (Rust), Master Sender e Client Copier (Python) em executáveis |
| `quick_test.bat` | **Teste rápido** - Inicia todos os componentes automaticamente em janelas separadas |
| `clean_build.bat` | **Limpeza** - Remove todos os artefatos de build para rebuild limpo |

### 📚 Documentação

| Arquivo | Descrição |
|---------|-----------|
| `QUICKSTART.md` | **Guia de início rápido** - 3 passos para começar a usar |
| `TESTING_GUIDE.md` | **Guia de testes** - Instruções detalhadas de configuração e teste |
| `ARCHITECTURE.md` | **Diagrama de arquitetura** - Fluxo de dados, endpoints, configurações |
| `TEST_CHECKLIST.md` | **Checklist de testes** - 24 testes para validação completa |
| `README.md` (este arquivo) | **Resumo geral** - Visão geral do sistema |

---

## 🏗️ Arquitetura do Sistema

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│  MT5 MASTER │ ──────▶ │ API SERVER  │ ──────▶ │ MT5 CLIENT  │
│             │         │   (Rust)    │         │             │
└─────────────┘         │  Port 8000  │         └─────────────┘
       │                └─────────────┘                │
       │                       │                       │
       ▼                       │                       ▼
┌─────────────┐                │                ┌─────────────┐
│   MASTER    │                │                │   CLIENT    │
│   SENDER    │────HTTP POST───┤                │   COPIER    │
│  (Python)   │                │                │  (Python)   │
└─────────────┘                └───WebSocket────└─────────────┘
```

### Componentes

1. **API Server (Rust/Axum)**
   - Servidor HTTP/WebSocket na porta 8000
   - Gerencia autenticação JWT
   - Broadcast de sinais para clientes
   - Banco de dados SQLite

2. **Master Sender (Python)**
   - Monitora conta MT5 Master
   - Detecta novas ordens, modificações e fechamentos
   - Envia sinais para API via HTTP POST

3. **Client Copier (Python)**
   - Conecta via WebSocket ao API Server
   - Recebe sinais em tempo real
   - Copia ordens na conta MT5 Client
   - Aplica safety rules

---

## 🚀 Como Usar

### Passo 1: Build
```bash
# Compilar todos os executáveis
build_test_exe.bat
```

Isso cria a pasta `dist_test/` com:
- `api_server.exe` (ou use `cargo run` em api_server/)
- `master_sender.exe`
- `client_copier.exe`
- `config_sender.json`
- `config_client.json`

### Passo 2: Configurar

Edite `dist_test/config_sender.json`:
```json
{
  "mt5": {
    "login": 12345678,
    "password": "sua_senha_master",
    "server": "seu_servidor"
  }
}
```

Edite `dist_test/config_client.json`:
```json
{
  "mt5": {
    "login": 87654321,
    "password": "sua_senha_client",
    "server": "seu_servidor"
  },
  "trade_copy": {
    "mode": "fix",
    "fixed_lot": 0.01
  }
}
```

### Passo 3: Testar

```bash
# Inicia todos os componentes automaticamente
quick_test.bat
```

Ou manualmente:
```bash
# Terminal 1: API Server
cd api_server
cargo run --release

# Terminal 2: Master Sender
cd dist_test
master_sender.exe

# Terminal 3: Client Copier
cd dist_test
client_copier.exe
```

### Passo 4: Validar

1. Abra uma ordem no MT5 Master
2. Verifique os logs:
   - `sender.log` - deve mostrar ordem detectada e enviada
   - `client.log` - deve mostrar ordem recebida e copiada
3. Confirme que a ordem aparece no MT5 Client

---

## ⚙️ Configurações Principais

### Modo de Cópia

**Volume Fixo:**
```json
"trade_copy": {
  "mode": "fix",
  "fixed_lot": 0.01
}
```

**Volume Proporcional:**
```json
"trade_copy": {
  "mode": "multiplier",
  "multiplier": 0.5  // 50% do volume do Master
}
```

### Safety Rules

```json
"trade_copy": {
  "max_slippage_points": 50,
  "max_spread_points": 20,
  "max_exposure_trades": 5,
  "max_exposure_lots": 10.0
},
"safety": {
  "max_drawdown_percent": 10
}
```

---

## 📊 Endpoints da API

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/token` | Login (retorna JWT) | ❌ |
| POST | `/users/public` | Criar usuário | ❌ |
| POST | `/signal/broadcast` | Enviar sinal | ✅ |
| POST | `/signal/close` | Fechar sinal | ✅ |
| GET | `/ws` | WebSocket | ✅ |
| GET | `/health` | Health check | ❌ |

---

## 🔍 Monitoramento

### Logs

- **sender.log** - Master Sender
  - Ordens detectadas
  - Sinais enviados
  - Erros de conexão

- **client.log** - Client Copier
  - Sinais recebidos
  - Ordens copiadas
  - Safety rules aplicadas

### Verificação de Saúde

```bash
# Verificar se API está rodando
curl http://localhost:8000/health
# Deve retornar: OK
```

---

## 🐛 Troubleshooting

### Problema: Executáveis não foram criados
**Solução:**
```bash
clean_build.bat
build_test_exe.bat
```

### Problema: "Failed to connect to MT5"
**Soluções:**
- Certifique-se que MT5 está aberto e logado
- Verifique credenciais em config
- Reinicie o MT5

### Problema: "Connection refused to API"
**Soluções:**
- Verifique se API Server está rodando
- Verifique se porta 8000 está livre: `netstat -ano | findstr :8000`
- Reinicie o API Server

### Problema: Ordem não foi copiada
**Soluções:**
- Verifique client.log para detalhes
- Verifique safety rules (spread, slippage)
- Verifique margem disponível
- Verifique se símbolo está disponível

---

## 📈 Fluxo de Dados

```
1. Ordem aberta no MT5 Master
   ↓
2. Master Sender detecta
   ↓
3. POST /signal/broadcast → API Server
   ↓
4. API Server salva no DB
   ↓
5. Broadcast via WebSocket
   ↓
6. Client Copier recebe
   ↓
7. Aplica safety rules
   ↓
8. Copia ordem no MT5 Client
```

---

## 🔐 Segurança

### Autenticação
- JWT tokens para autenticação
- Credenciais em arquivos de configuração (não commitar!)

### Proteção dos Executáveis
- PyInstaller com `--onefile`
- Opção `--key` para ofuscação básica
- Para produção: considere PyArmor

### Safety Rules
- Max spread, slippage, exposure
- Max drawdown protection
- Validações de margem e símbolo

---

## 📦 Estrutura de Pastas

```
aibot/backend/copy/
│
├── api_server/                  # Servidor Rust
│   ├── src/
│   │   ├── main.rs
│   │   ├── handlers/
│   │   ├── models/
│   │   ├── db/
│   │   └── auth/
│   └── Cargo.toml
│
├── master_sender/               # Master Sender
│   ├── main_sender.py
│   ├── sender_service.py
│   ├── mt5_connector.py
│   └── config_sender.json
│
├── client_copier/               # Client Copier
│   ├── main_client.py
│   ├── client_service.py
│   ├── mt5_connector.py
│   ├── safety.py
│   └── config_client.json
│
├── dist_test/                   # Executáveis (gerado)
│   ├── master_sender.exe
│   ├── client_copier.exe
│   ├── config_sender.json
│   └── config_client.json
│
├── build_test_exe.bat          # Build script
├── quick_test.bat              # Test script
├── clean_build.bat             # Clean script
│
└── Documentação/
    ├── QUICKSTART.md
    ├── TESTING_GUIDE.md
    ├── ARCHITECTURE.md
    ├── TEST_CHECKLIST.md
    └── README.md (este arquivo)
```

---

## 🎯 Próximos Passos

### Fase 1: Validação ✅
- [x] Compilar executáveis
- [x] Configurar contas MT5
- [x] Testar cópia básica
- [x] Validar safety rules

### Fase 2: Testes Avançados
- [ ] Teste com múltiplos clientes
- [ ] Teste de reconexão
- [ ] Teste de stress (múltiplas ordens)
- [ ] Teste de latência

### Fase 3: Produção
- [ ] Build com GUI (Tauri)
- [ ] Deploy em VPS
- [ ] Monitoramento contínuo
- [ ] Backup e recovery

---

## 📞 Recursos

| Recurso | Localização |
|---------|-------------|
| Início Rápido | `QUICKSTART.md` |
| Guia de Testes | `TESTING_GUIDE.md` |
| Arquitetura | `ARCHITECTURE.md` |
| Checklist | `TEST_CHECKLIST.md` |
| Logs | `dist_test/*.log` |

---

## ⚡ Comandos Rápidos

```bash
# Build completo
build_test_exe.bat

# Teste rápido
quick_test.bat

# Rebuild limpo
clean_build.bat
build_test_exe.bat

# Verificar saúde da API
curl http://localhost:8000/health

# Ver logs em tempo real (PowerShell)
Get-Content dist_test\sender.log -Wait -Tail 20
Get-Content dist_test\client.log -Wait -Tail 20
```

---

## 💡 Dicas Importantes

1. **Sempre teste em conta demo primeiro**
2. **Verifique os logs antes de reportar problemas**
3. **Mantenha backups das configurações**
4. **Use safety rules apropriadas para seu risco**
5. **Monitore a latência regularmente**
6. **Nunca commite arquivos com senhas reais**

---

## ✅ Status do Projeto

- ✅ API Server (Rust) - Funcional
- ✅ Master Sender (Python) - Funcional
- ✅ Client Copier (Python) - Funcional
- ✅ Build Scripts - Completo
- ✅ Documentação - Completa
- ✅ Testes Básicos - Validados
- ⏳ Testes Avançados - Pendente
- ⏳ GUI (Tauri) - Pendente
- ⏳ Deploy Produção - Pendente

---

**Versão:** 1.0.0  
**Data:** 2026-01-01  
**Status:** ✅ Pronto para Testes

---

**Boa sorte com seu Trade Copier! 🚀📈**
