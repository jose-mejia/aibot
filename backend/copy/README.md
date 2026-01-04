# 🚀 Zulfinance CopyTrading System

Sistema profissional de copy trading para MetaTrader 5 com arquitetura cliente-servidor.

**Versão:** 1.0  
**Status:** ✅ Estável e Pronto para Testes

---

## 📚 Documentação

**Toda a documentação técnica está organizada em:**

### 👉 **[`docs/`](docs/README.md)** ← CLIQUE AQUI

Documentos principais:
- **[Auditoria de Fluxo de Ordens](docs/AUDIT_ORDER_FLOW.md)** - Checklist completo de testes
- **[Detecção de Ordens](docs/ORDER_DETECTION.md)** - Como funciona (manual e bot)
- **[Segurança do Banco de Dados](docs/DATABASE_SECURITY.md)** - Política de segurança
- **[Release v1.0](docs/RELEASE_v1.0.md)** - O que foi implementado

---

## 🏗️ Arquitetura

```
Master Trader (MT5) → Master Sender (Python) → API Server (Rust) → Client Copier (Python) → Client MT5
```

### Componentes:
- **Master Sender** - Detecta ordens no MT5 Master (manual ou bot)
- **API Server** - Backend Rust com segurança multi-camada
- **Client Copier** - Replica ordens no MT5 Client com SafetyGuard
- **Database** - SQLite único e oficial (`api_server/aibot.db`)

---

## ⚡ Quick Start

### 1. Iniciar API Server
```powershell
cd api_server
cargo run
```

### 2. Iniciar Master Sender
```powershell
cd master_sender/gui
npm run tauri dev
```

### 3. Iniciar Client Copier
```powershell
cd client_copier/gui
npm run tauri dev
```

### 4. Configurar Perfis
- Preencher **MT5 ID** e **MT5 Path** em ambos os apps
- Salvar configurações

### 5. Testar
- Abrir ordem manual no MT5 Master
- Verificar cópia no MT5 Client

**Documentação completa:** [`docs/AUDIT_ORDER_FLOW.md`](docs/AUDIT_ORDER_FLOW.md)

---

## ✅ Features Implementadas

- ✅ Detecção automática de ordens (manual e bot)
- ✅ Copy trading em tempo real via WebSocket
- ✅ Segurança multi-camada (JWT + HMAC + Role-based)
- ✅ SafetyGuard (limites, margem, SL)
- ✅ Configuração dinâmica de MT5 Path
- ✅ Banco de dados único e protegido
- ✅ Logs detalhados para debug
- ✅ Arredondamento de preços (evita "Invalid Price")

---

## 🔐 Segurança

O sistema implementa **4 camadas de segurança**:
1. **JWT Authentication** - Autenticação de usuários
2. **Role-Based Access** - Apenas MASTER pode broadcast
3. **HMAC-SHA256 Signature** - Integridade de dados
4. **Timestamp Validation** - Anti-replay attacks

**Leia:** [`docs/DATABASE_SECURITY.md`](docs/DATABASE_SECURITY.md)

---

## 🧪 Testes

**Checklist completo de testes:** [`docs/AUDIT_ORDER_FLOW.md`](docs/AUDIT_ORDER_FLOW.md)

Testes incluem:
- ✅ Ordem de compra (BUY Market)
- ✅ Ordem pendente (BUY LIMIT)
- ✅ Modificação de SL/TP
- ✅ Fechamento de ordem
- ✅ Múltiplas ordens simultâneas
- ✅ Reconexão após queda
- ✅ Testes de segurança

---

## 📞 Suporte

**Problemas comuns?** Consulte [`docs/README.md`](docs/README.md) - Seção "Suporte e Troubleshooting"

**Dúvidas sobre código?** Consulte [`docs/AUDIT_ORDER_FLOW.md`](docs/AUDIT_ORDER_FLOW.md)

---

## 🤝 Contribuindo

1. Leia [`docs/GITHUB_GUIDE.md`](docs/GITHUB_GUIDE.md)
2. Consulte [`docs/RESPONSIBILITY_AREAS.md`](docs/RESPONSIBILITY_AREAS.md)
3. Siga padrões de segurança em [`docs/DATABASE_SECURITY.md`](docs/DATABASE_SECURITY.md)

---

## 📊 Status do Projeto

| Componente | Status | Versão |
|------------|--------|--------|
| API Server | ✅ Estável | 1.0 |
| Master Sender | ✅ Estável | 1.0 |
| Client Copier | ✅ Estável | 1.0 |
| Documentação | ✅ Completa | 1.0 |
| Testes | ⏳ Em andamento | - |

---

**Desenvolvido por:** Equipe Zulfinance  
**Última Atualização:** 2026-01-04
