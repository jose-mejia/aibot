# 📚 Documentação Técnica - Zulfinance CopyTrading System

**Versão:** 1.0  
**Última Atualização:** 2026-01-04

---

## 📖 Índice de Documentos

### 🏗️ Arquitetura e Design
- **[DESIGN_SYSTEM.md](DESIGN_SYSTEM.md)** - Sistema de design e padrões visuais
- **[DATABASE_OFFICIAL.md](DATABASE_OFFICIAL.md)** - Banco de dados oficial e regras de acesso
- **[DATABASE_SECURITY.md](DATABASE_SECURITY.md)** - Política de segurança do banco de dados

### 🔍 Auditoria e Testes
- **[AUDIT_ORDER_FLOW.md](AUDIT_ORDER_FLOW.md)** - Auditoria completa do fluxo de ordens + Checklist de testes

### 📋 Planejamento e Gestão
- **[DELEGATION_PLAN.md](DELEGATION_PLAN.md)** - Plano de delegação de tarefas
- **[RELEASE_v1.0.md](RELEASE_v1.0.md)** - Notas de release da versão 1.0
- **[RESPONSIBILITY_AREAS.md](RESPONSIBILITY_AREAS.md)** - Áreas de responsabilidade do projeto
- **[NEXT_STEPS.md](NEXT_STEPS.md)** - Próximos passos do desenvolvimento

### 🛠️ Workflows e Procedimentos
- **[WORKFLOW_MT5_PATH.md](WORKFLOW_MT5_PATH.md)** - Workflow de configuração do MT5 Path
- **[GITHUB_GUIDE.md](GITHUB_GUIDE.md)** - Guia de uso do GitHub para o projeto
- **[GITHUB_SETUP_COMPLETE.md](GITHUB_SETUP_COMPLETE.md)** - Configuração completa do GitHub
- **[CHECK_SERVER_VERSION.md](CHECK_SERVER_VERSION.md)** - Como verificar versão do servidor

---

## 🎯 Documentos por Público-Alvo

### Para Desenvolvedores
1. **[AUDIT_ORDER_FLOW.md](AUDIT_ORDER_FLOW.md)** - Entenda o fluxo completo de ordens
2. **[DATABASE_SECURITY.md](DATABASE_SECURITY.md)** - Regras de segurança obrigatórias
3. **[WORKFLOW_MT5_PATH.md](WORKFLOW_MT5_PATH.md)** - Como implementar features relacionadas ao MT5

### Para Gestores de Projeto
1. **[RELEASE_v1.0.md](RELEASE_v1.0.md)** - O que foi entregue na v1.0
2. **[DELEGATION_PLAN.md](DELEGATION_PLAN.md)** - Como delegar tarefas
3. **[RESPONSIBILITY_AREAS.md](RESPONSIBILITY_AREAS.md)** - Quem é responsável por quê

### Para Testadores (QA)
1. **[AUDIT_ORDER_FLOW.md](AUDIT_ORDER_FLOW.md)** - Checklist completo de testes
2. **[CHECK_SERVER_VERSION.md](CHECK_SERVER_VERSION.md)** - Validar versão antes de testar

### Para Designers
1. **[DESIGN_SYSTEM.md](DESIGN_SYSTEM.md)** - Padrões visuais e componentes

---

## 🔐 Documentos de Segurança (CRÍTICOS)

⚠️ **LEITURA OBRIGATÓRIA** antes de fazer qualquer alteração no código:

1. **[DATABASE_SECURITY.md](DATABASE_SECURITY.md)**
   - Política de acesso ao banco de dados
   - Prevenção de ataques
   - Arquitetura de segurança

2. **[DATABASE_OFFICIAL.md](DATABASE_OFFICIAL.md)**
   - Banco de dados único e oficial
   - Regras de conexão
   - Scripts administrativos

---

## 📊 Fluxo de Trabalho Recomendado

### Para Novos Desenvolvedores:
1. Leia **[GITHUB_GUIDE.md](GITHUB_GUIDE.md)** - Aprenda a usar o GitHub
2. Leia **[AUDIT_ORDER_FLOW.md](AUDIT_ORDER_FLOW.md)** - Entenda a arquitetura
3. Leia **[DATABASE_SECURITY.md](DATABASE_SECURITY.md)** - Regras de segurança
4. Consulte **[RESPONSIBILITY_AREAS.md](RESPONSIBILITY_AREAS.md)** - Veja sua área

### Para Implementar Nova Feature:
1. Consulte **[DELEGATION_PLAN.md](DELEGATION_PLAN.md)** - Veja se há tarefa relacionada
2. Leia documentação técnica relevante
3. Implemente seguindo padrões de segurança
4. Teste usando **[AUDIT_ORDER_FLOW.md](AUDIT_ORDER_FLOW.md)** como referência
5. Documente mudanças

### Para Resolver Bug:
1. Consulte **[CHECK_SERVER_VERSION.md](CHECK_SERVER_VERSION.md)** - Valide versão
2. Consulte **[AUDIT_ORDER_FLOW.md](AUDIT_ORDER_FLOW.md)** - Entenda o fluxo
3. Corrija e teste
4. Atualize documentação se necessário

---

## 🆘 Suporte e Troubleshooting

### Problemas Comuns:

**"Erro 500 ao salvar Profile"**
→ Consulte: [CHECK_SERVER_VERSION.md](CHECK_SERVER_VERSION.md)

**"Ordens não estão sendo copiadas"**
→ Consulte: [AUDIT_ORDER_FLOW.md](AUDIT_ORDER_FLOW.md) - Seção "Checklist de Testes"

**"Banco de dados não encontrado"**
→ Consulte: [DATABASE_OFFICIAL.md](DATABASE_OFFICIAL.md)

**"Erro de segurança/acesso negado"**
→ Consulte: [DATABASE_SECURITY.md](DATABASE_SECURITY.md)

---

## 📝 Contribuindo com a Documentação

### Ao adicionar novo documento:
1. Coloque na pasta `docs/`
2. Atualize este README.md
3. Use formato Markdown (.md)
4. Inclua data de criação/atualização
5. Adicione ao índice apropriado

### Padrão de Nomenclatura:
- `NOME_DO_DOCUMENTO.md` (UPPERCASE com underscores)
- Seja descritivo e conciso
- Evite abreviações obscuras

---

## 📞 Contato

**Dúvidas sobre documentação?**
- Abra uma Issue no GitHub
- Consulte [GITHUB_GUIDE.md](GITHUB_GUIDE.md) para instruções

---

**Mantido por:** Equipe Zulfinance  
**Última Revisão:** 2026-01-04
