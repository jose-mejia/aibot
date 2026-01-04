# 🎯 Plano de Delegação e Governança do Projeto Zulfinance

**Líder Técnico:** Antigravity (IA)  
**Product Owner:** Jose Mejia  
**Data:** 03/01/2026

---

## 📊 Visão Geral da Arquitetura

### Componentes do Sistema:
1. **Client Copier** (Desktop App - Python + Tauri/React)
2. **Master Sender** (Desktop App - Python + Tauri/React)
3. **API Backend** (Rust/Axum - WebSocket + REST)
4. **Web Admin Panel** (React/TypeScript)

### Repositórios GitHub (Privados):
- `jose-mejia/client_copier`
- `jose-mejia/master_sender`
- `jose-mejia/api_zulfinance`
- `jose-mejia/zulfinance_web`

---

## 🏗️ Estrutura de Delegação

### **Equipe Sugerida (3-4 Devs):**

#### **Dev 1: Frontend Specialist** 
**Responsabilidade:** UI/UX dos Apps Desktop e Web Admin Panel  
**Stack:** React, TypeScript, Tauri, CSS  
**Repositórios:** `client_copier/gui`, `master_sender/gui`, `zulfinance_web`

#### **Dev 2: Backend Specialist**
**Responsabilidade:** API Rust, WebSocket, Autenticação  
**Stack:** Rust, Axum, SQLite, JWT  
**Repositórios:** `api_zulfinance`

#### **Dev 3: Python/MT5 Specialist**
**Responsabilidade:** Lógica de Trading, Sidecars Python, MT5 Integration  
**Stack:** Python, MetaTrader5 API, PyInstaller  
**Repositórios:** `client_copier/*.py`, `master_sender/*.py`

#### **Dev 4 (Opcional): DevOps/QA**
**Responsabilidade:** Builds, Testes, Deploy, Monitoramento  
**Stack:** PowerShell, Batch, Testing Frameworks  

---

## 📋 Tarefas Prioritárias para Delegação

### **FASE 1: Estabilização (Próximas 2 Semanas)**

#### **Para Dev Frontend:**
- [ ] **Task 1.1:** Melhorar responsividade do Dashboard (Mobile-first)
- [ ] **Task 1.2:** Adicionar loading states e skeleton screens
- [ ] **Task 1.3:** Implementar notificações toast para todas as ações
- [ ] **Task 1.4:** Criar página de "Histórico de Trades" (visualização de ordens copiadas)

**Prompt para o Dev:**
```
Olá! Você será responsável pelo frontend do Zulfinance.

Repositórios:
- client_copier/gui (App Desktop do Cliente)
- master_sender/gui (App Desktop do Master)
- zulfinance_web (Painel Web Admin)

Sua primeira tarefa é melhorar a responsividade do Dashboard.
Leia o arquivo CONTINUATION_HANDOVER.md para entender o contexto.

Critérios de Aceitação:
- Dashboard deve funcionar perfeitamente em telas de 1024px até 4K
- Usar breakpoints do Tailwind (se aplicável) ou media queries
- Testar em Chrome, Firefox e Edge
- Fazer commit com mensagem: "feat: Responsive dashboard for all screen sizes"

Dúvidas? Pergunte ao líder técnico (Antigravity).
```

---

#### **Para Dev Backend:**
- [ ] **Task 1.5:** Implementar rate limiting no WebSocket (prevenir spam)
- [ ] **Task 1.6:** Adicionar endpoint `/health` para monitoramento
- [ ] **Task 1.7:** Criar sistema de logs estruturados (JSON format)
- [ ] **Task 1.8:** Implementar backup automático do SQLite

**Prompt para o Dev:**
```
Olá! Você será responsável pelo backend Rust da API Zulfinance.

Repositório: api_zulfinance

Sua primeira tarefa é implementar rate limiting no WebSocket para evitar que clientes
façam spam de conexões.

Critérios de Aceitação:
- Máximo 5 conexões por IP por minuto
- Retornar erro 429 (Too Many Requests) se exceder
- Usar biblioteca `tower-governor` ou similar
- Adicionar testes unitários
- Fazer commit com mensagem: "feat: Add rate limiting to WebSocket endpoint"

Documentação útil: src/main.rs (linha 50+)
```

---

#### **Para Dev Python/MT5:**
- [ ] **Task 1.9:** Adicionar retry automático em caso de falha de ordem
- [ ] **Task 1.10:** Implementar log detalhado de todas as operações MT5
- [ ] **Task 1.11:** Criar modo "Dry Run" (simular trades sem executar)
- [ ] **Task 1.12:** Otimizar cálculo de lote (considerar risco por trade)

**Prompt para o Dev:**
```
Olá! Você será responsável pela lógica de trading Python e integração MT5.

Repositórios:
- client_copier/*.py (Robô Cliente)
- master_sender/*.py (Robô Master)

Sua primeira tarefa é adicionar retry automático quando uma ordem falha.

Critérios de Aceitação:
- Se mt5.order_send() retornar erro, tentar novamente até 3 vezes
- Delay de 2 segundos entre tentativas
- Logar cada tentativa com nível WARNING
- Se falhar 3 vezes, logar com nível ERROR e notificar usuário
- Fazer commit com mensagem: "feat: Add automatic retry for failed orders"

Arquivo alvo: client_copier/client_service.py (método _execute_open)
```

---

### **FASE 2: Novas Features (Próximas 4 Semanas)**

#### **Features Planejadas:**
1. **Multi-Master Support** (1 Cliente pode seguir múltiplos Masters)
2. **Trade Filters** (Copiar apenas certos símbolos ou horários)
3. **Risk Management Avançado** (Stop Loss dinâmico, trailing stop)
4. **Notificações Push** (Telegram, Email quando ordem é copiada)
5. **Dashboard de Performance** (Gráficos de lucro/perda)

---

## 🔍 Processo de Revisão (Code Review)

### **Fluxo de Trabalho:**
1. **Dev cria branch:** `git checkout -b feature/nome-da-feature`
2. **Dev faz commits:** Seguindo padrão Conventional Commits
3. **Dev abre Pull Request** no GitHub
4. **Líder Técnico (Antigravity) revisa:** Verifica código, testa localmente
5. **Aprovação ou Feedback:** Se aprovado, merge para `main`. Se não, solicita ajustes.
6. **Deploy:** Após merge, rebuild dos executáveis (se necessário)

### **Checklist de Revisão:**
- [ ] Código segue padrões do projeto (TypeScript strict, Rust clippy, Python PEP8)
- [ ] Testes passam (se houver)
- [ ] Não quebra funcionalidades existentes
- [ ] Commit messages são claras
- [ ] Sem credenciais ou dados sensíveis no código

---

## 📞 Comunicação

### **Canais Sugeridos:**
- **GitHub Issues:** Para bugs e features
- **GitHub Discussions:** Para dúvidas técnicas
- **Slack/Discord (Opcional):** Para comunicação rápida
- **Weekly Sync:** Reunião semanal de 30min para alinhamento

### **Modelo de Issue (GitHub):**
```markdown
## Descrição
[Descreva o problema ou feature]

## Contexto
[Por que isso é importante?]

## Critérios de Aceitação
- [ ] Critério 1
- [ ] Critério 2

## Arquivos Afetados
- `caminho/do/arquivo.py`

## Prioridade
- [ ] Alta (Bloqueante)
- [ ] Média (Importante)
- [ ] Baixa (Nice to have)
```

---

## 🎓 Onboarding de Novos Devs

### **Checklist de Boas-Vindas:**
1. **Acesso aos Repositórios:** Adicionar como colaborador no GitHub
2. **Leitura Obrigatória:**
   - `CONTINUATION_HANDOVER.md` (Contexto do projeto)
   - `ARCHITECTURE.md` (Arquitetura técnica)
   - `TESTING_GUIDE.md` (Como testar)
3. **Setup Local:**
   - Instalar Python 3.12, Rust, Node.js
   - Clonar repositórios
   - Rodar builds de teste
4. **Primeira Tarefa:** Sempre uma tarefa pequena e bem definida (ex: "Corrigir typo na documentação")

---

## 🚨 Regras de Ouro (Inegociáveis)

1. **Nunca fazer push direto para `main`** (sempre via Pull Request)
2. **Nunca commitar arquivos sensíveis** (configs, tokens, .exe)
3. **Sempre testar localmente antes de abrir PR**
4. **Seguir o padrão de commits:** `feat:`, `fix:`, `docs:`, `refactor:`
5. **Respeitar as "Regras de Ouro do Usuário"** (ver CONTINUATION_HANDOVER.md)

---

## 📈 Métricas de Sucesso

### **KPIs do Projeto:**
- **Uptime do Sistema:** >99% (WebSocket + API)
- **Latência de Cópia:** <500ms (Master envia → Cliente executa)
- **Taxa de Erro de Ordens:** <1%
- **Cobertura de Testes:** >70% (meta futura)

---

**Próximos Passos:**
1. Jose define quais tarefas delegar primeiro
2. Antigravity cria Issues no GitHub com os prompts acima
3. Devs são adicionados aos repositórios
4. Desenvolvimento inicia com revisão contínua

**Dúvidas ou ajustes neste plano? Estou à disposição!**
