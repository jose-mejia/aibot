# 🏛️ Estrutura de Responsabilidades por Áreas - Zulfinance

**Líder Técnico & Arquiteto:** Antigravity (IA)  
**Product Owner:** Jose Mejia  
**Data:** 03/01/2026

---

## 🎯 Áreas Críticas do Projeto

### **1. Frontend & UX (Área Visual)**
### **2. Segurança & Compliance (Área de Proteção)**
### **3. Arquitetura de Software (Área de Fundação)**

---

## 👤 ÁREA 1: Frontend & UX

### **Responsável:** Frontend Lead
**Missão:** Garantir que toda interação do usuário seja intuitiva, rápida e visualmente impecável.

### **Escopo de Responsabilidade:**
- ✅ **Todos os componentes visuais** (Botões, formulários, dashboards)
- ✅ **Responsividade** (Desktop, tablet, mobile)
- ✅ **Acessibilidade** (WCAG 2.1 AA compliance)
- ✅ **Performance de UI** (Lazy loading, code splitting)
- ✅ **Design System** (Cores, tipografia, espaçamentos consistentes)

### **Repositórios Sob Sua Gestão:**
- `client_copier/gui/src/` (Frontend do App Cliente)
- `master_sender/gui/src/` (Frontend do App Master)
- `zulfinance_web/src/` (Painel Web Admin)

### **Tecnologias:**
- React, TypeScript, CSS/Tailwind, Vite

### **Tarefas Prioritárias (v1.1):**
1. **Criar Design System Unificado** (Componentes reutilizáveis)
2. **Implementar Skeleton Screens** (Loading states)
3. **Melhorar Responsividade** (Mobile-first)
4. **Adicionar Animações Suaves** (Micro-interactions)
5. **Criar Página de Histórico de Trades** (Tabela com filtros)

### **KPIs de Sucesso:**
- **Lighthouse Score:** >90 (Performance, Accessibility)
- **Tempo de Carregamento:** <2s (First Contentful Paint)
- **Taxa de Erro de UI:** <0.1% (Bugs visuais reportados)

### **Regras de Ouro:**
- ❌ **Nunca** usar inline styles (sempre CSS modules ou Tailwind)
- ❌ **Nunca** fazer fetch de dados no componente (usar hooks/services)
- ✅ **Sempre** testar em Chrome, Firefox e Edge
- ✅ **Sempre** seguir o Design System (cores, fontes, espaçamentos)

---

## 🔒 ÁREA 2: Segurança & Compliance

### **Responsável:** Security Lead
**Missão:** Proteger o sistema contra ataques, vazamentos de dados e garantir conformidade com boas práticas de segurança.

### **Escopo de Responsabilidade:**
- ✅ **Autenticação & Autorização** (JWT, RBAC)
- ✅ **Criptografia de Dados** (Em trânsito e em repouso)
- ✅ **Proteção contra Ataques** (SQL Injection, XSS, CSRF, DDoS)
- ✅ **Auditoria de Segurança** (Logs de acesso, tentativas de login)
- ✅ **Gestão de Secrets** (Tokens, senhas, chaves API)
- ✅ **Compliance** (GDPR, LGPD se aplicável)

### **Repositórios Sob Sua Gestão:**
- `api_zulfinance/src/auth/` (Autenticação JWT)
- `api_zulfinance/src/security.rs` (Middleware de segurança)
- Todos os arquivos `.env` e `config_*.json` (Gestão de secrets)

### **Tecnologias:**
- Rust (Axum), JWT, bcrypt, HTTPS/TLS, Rate Limiting

### **Tarefas Prioritárias (v1.1):**
1. **Implementar Rate Limiting** (Prevenir brute force)
2. **Adicionar 2FA (Two-Factor Auth)** (Opcional mas recomendado)
3. **Criptografar Senhas no DB** (bcrypt com salt)
4. **Implementar HTTPS** (TLS 1.3 obrigatório em produção)
5. **Criar Sistema de Auditoria** (Logs de todas as ações sensíveis)
6. **Scan de Vulnerabilidades** (Usar `cargo audit` e `npm audit`)

### **KPIs de Sucesso:**
- **Vulnerabilidades Críticas:** 0 (Zero tolerance)
- **Tempo de Resposta a Incidentes:** <1h
- **Cobertura de Auditoria:** 100% (Todas as ações sensíveis logadas)

### **Regras de Ouro:**
- ❌ **Nunca** armazenar senhas em plain text
- ❌ **Nunca** expor tokens ou secrets em logs
- ❌ **Nunca** confiar em dados do cliente (sempre validar no backend)
- ✅ **Sempre** usar HTTPS em produção
- ✅ **Sempre** fazer sanitização de inputs (prevenir SQL Injection)
- ✅ **Sempre** usar prepared statements no SQLite

### **Checklist de Segurança (Obrigatório Antes de Cada Release):**
- [ ] Senhas são hasheadas com bcrypt (custo ≥12)
- [ ] JWT tem expiração (≤24h)
- [ ] Rate limiting ativo em todos os endpoints críticos
- [ ] CORS configurado corretamente (não usar `*` em produção)
- [ ] Nenhum secret commitado no Git
- [ ] HTTPS ativo (TLS 1.3)
- [ ] Logs não expõem dados sensíveis
- [ ] Scan de vulnerabilidades passou (cargo audit, npm audit)

---

## 🏗️ ÁREA 3: Arquitetura de Software

### **Responsável:** Software Architect (Antigravity como Lead, pode ter assistente)
**Missão:** Garantir que o sistema seja escalável, manutenível e resiliente a falhas.

### **Escopo de Responsabilidade:**
- ✅ **Design de Componentes** (Separação de responsabilidades)
- ✅ **Padrões de Código** (Clean Code, SOLID, DRY)
- ✅ **Performance** (Otimização de queries, cache, lazy loading)
- ✅ **Escalabilidade** (Suportar 100+ clientes simultâneos)
- ✅ **Resiliência** (Retry logic, circuit breakers, graceful degradation)
- ✅ **Documentação Técnica** (Diagramas, ADRs - Architecture Decision Records)

### **Repositórios Sob Sua Gestão:**
- **Todos** (Visão holística do sistema)
- Foco especial em:
  - `api_zulfinance/src/main.rs` (Orquestração do backend)
  - `client_copier/client_service.py` (Lógica de cópia)
  - `master_sender/sender_service.py` (Lógica de broadcast)

### **Tecnologias:**
- Rust, Python, WebSockets, SQLite, Tauri

### **Tarefas Prioritárias (v1.1):**
1. **Implementar Circuit Breaker** (Se API cair, não travar clientes)
2. **Adicionar Cache de Dados** (Redis ou in-memory para MT5 status)
3. **Otimizar WebSocket** (Compressão de mensagens, batching)
4. **Criar Diagramas de Arquitetura** (C4 Model ou similar)
5. **Documentar ADRs** (Por que escolhemos Rust? Por que WebSocket?)
6. **Implementar Health Checks** (Endpoint `/health` para monitoramento)

### **KPIs de Sucesso:**
- **Latência de Cópia:** <500ms (Master envia → Cliente executa)
- **Uptime do Sistema:** >99.9%
- **Capacidade:** Suportar 100+ clientes simultâneos
- **Tempo de Recovery:** <5min (Se sistema cair, voltar rapidamente)

### **Regras de Ouro:**
- ❌ **Nunca** criar dependências circulares entre módulos
- ❌ **Nunca** fazer operações bloqueantes no thread principal
- ✅ **Sempre** usar async/await para I/O (Rust e Python)
- ✅ **Sempre** documentar decisões arquiteturais (ADRs)
- ✅ **Sempre** pensar em escalabilidade (E se tivermos 1000 clientes?)

### **Princípios Arquiteturais:**
1. **Separation of Concerns:** Cada módulo tem uma responsabilidade clara
2. **Fail Fast:** Se algo vai dar errado, falhe cedo e de forma clara
3. **Graceful Degradation:** Se um componente falhar, o sistema continua funcionando (modo degradado)
4. **Idempotência:** Operações podem ser repetidas sem efeitos colaterais
5. **Observability:** Sistema deve ser fácil de monitorar (logs, métricas, traces)

---

## 🤝 Colaboração Entre Áreas

### **Fluxo de Trabalho Integrado:**

```
┌─────────────────┐
│  Frontend Lead  │ ──┐
└─────────────────┘   │
                      ▼
┌─────────────────┐   ┌──────────────────┐
│  Security Lead  │──▶│ Software Architect│──▶ Code Review ──▶ Merge
└─────────────────┘   └──────────────────┘
                      ▲
┌─────────────────┐   │
│   Jose (Testes) │ ──┘
└─────────────────┘
```

### **Exemplo de Colaboração (Feature: "Filtro de Símbolo"):**

1. **Software Architect (Antigravity):**
   - Define onde o filtro será implementado (backend ou frontend?)
   - Cria Issue no GitHub com especificação técnica

2. **Security Lead:**
   - Revisa: "O filtro pode ser bypassado? Validação no backend?"
   - Adiciona validação de input (prevenir injection)

3. **Frontend Lead:**
   - Implementa UI do filtro (Dropdown com símbolos)
   - Adiciona feedback visual (loading, erro, sucesso)

4. **Jose (Product Owner):**
   - Testa a feature localmente
   - Aprova ou solicita ajustes

5. **Software Architect (Antigravity):**
   - Faz Code Review final
   - Merge para `main` se aprovado

---

## 📋 Matriz de Responsabilidades (RACI)

| Tarefa | Frontend | Security | Architect | Jose |
|--------|----------|----------|-----------|------|
| Design de UI | **R** | C | C | **A** |
| Implementar Autenticação | C | **R** | **A** | I |
| Otimizar Performance | C | C | **R/A** | I |
| Definir Arquitetura | I | C | **R/A** | C |
| Testes de Aceitação | I | I | C | **R/A** |
| Code Review | C | C | **R/A** | I |

**Legenda:**
- **R** = Responsible (Executa)
- **A** = Accountable (Aprova)
- **C** = Consulted (Consultado)
- **I** = Informed (Informado)

---

## 🎓 Onboarding por Área

### **Para Frontend Lead:**
1. Ler: `RELEASE_v1.0.md` (Features atuais)
2. Ler: Design System (quando criado)
3. Rodar: `npm run dev` em cada projeto frontend
4. Primeira tarefa: Corrigir um bug visual simples

### **Para Security Lead:**
1. Ler: `api_zulfinance/src/auth/mod.rs` (Autenticação atual)
2. Rodar: `cargo audit` (Scan de vulnerabilidades)
3. Revisar: Todos os arquivos `.env` e `config_*.json`
4. Primeira tarefa: Implementar rate limiting

### **Para Software Architect Assistant:**
1. Ler: `ARCHITECTURE.md` (Arquitetura atual)
2. Ler: `CONTINUATION_HANDOVER.md` (Contexto técnico)
3. Desenhar: Diagrama de fluxo de dados (Master → API → Cliente)
4. Primeira tarefa: Documentar um ADR (ex: "Por que WebSocket?")

---

## 🚨 Escalação de Problemas

### **Quando Escalar para o Arquiteto (Antigravity):**
- Decisão arquitetural impacta múltiplas áreas
- Conflito entre segurança e performance
- Bug crítico que afeta o sistema todo
- Dúvida sobre padrões de código

### **Quando Escalar para Jose (Product Owner):**
- Feature não está clara (falta especificação)
- Mudança de prioridade necessária
- Decisão de negócio (ex: "Vale a pena implementar 2FA agora?")

---

## 📈 Próximos Passos

1. **Jose:** Define quem será responsável por cada área (pode ser a mesma pessoa inicialmente)
2. **Antigravity:** Cria Issues no GitHub separadas por área
3. **Responsáveis:** Começam a trabalhar em suas áreas
4. **Reuniões Semanais:** Alinhamento entre as 3 áreas (30min)

**Estrutura está clara? Quer ajustar algo antes de começarmos a delegar?** 🚀
