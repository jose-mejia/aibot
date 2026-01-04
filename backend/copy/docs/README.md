# 📚 Documentação Técnica - Zulfinance CopyTrading

**Versão:** 1.0  
**Última Atualização:** 2026-01-04

---

## 📂 Estrutura de Documentação

```
docs/
├── flows/          → Fluxos de operação (OPEN, MODIFY, CLOSE)
├── features/       → Features individuais (SafetyGuard, MT5 Path, etc)
├── architecture/   → Arquitetura do sistema
├── security/       → Documentação de segurança
├── testing/        → Guias e checklists de teste
└── README.md       → Este arquivo
```

---

## 🔄 FLUXOS DE OPERAÇÃO

### Fluxos Principais
- **[FLOW_OPEN_ORDER.md](flows/FLOW_OPEN_ORDER.md)** - Abertura de ordem (13 etapas detalhadas)
- **[FLOW_MODIFY.md](flows/FLOW_MODIFY.md)** - Modificação de SL/TP
- **[FLOW_CLOSE.md](flows/FLOW_CLOSE.md)** - Fechamento de ordem

### Como Usar
Cada fluxo contém:
- ✅ Diagrama visual
- ✅ Detalhamento por etapa
- ✅ Código-fonte relevante
- ✅ Métricas de performance
- ✅ Possíveis erros e soluções
- ✅ Checklist de teste

---

## 🎯 FEATURES

### Segurança
- **[DATABASE_SECURITY.md](security/DATABASE_SECURITY.md)** - Política de segurança do banco
- **[DATABASE_OFFICIAL.md](DATABASE_OFFICIAL.md)** - Banco de dados único oficial

### Funcionalidades
- **[ORDER_DETECTION.md](ORDER_DETECTION.md)** - Detecção de ordens (manual e bot)
- **[WORKFLOW_MT5_PATH.md](WORKFLOW_MT5_PATH.md)** - Configuração dinâmica de MT5 Path

---

## 🧪 TESTES

### Guias de Teste
- **[AUDIT_ORDER_FLOW.md](AUDIT_ORDER_FLOW.md)** - Auditoria completa + Checklist de 8 testes

### Como Testar
1. Leia o fluxo correspondente em `flows/`
2. Execute o checklist em `AUDIT_ORDER_FLOW.md`
3. Documente resultados

---

## 🏗️ ARQUITETURA

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Visão geral da arquitetura
- **[DESIGN_SYSTEM.md](DESIGN_SYSTEM.md)** - Sistema de design

---

## 📋 GESTÃO DE PROJETO

- **[RELEASE_v1.0.md](RELEASE_v1.0.md)** - Notas de release
- **[DELEGATION_PLAN.md](DELEGATION_PLAN.md)** - Plano de delegação
- **[RESPONSIBILITY_AREAS.md](RESPONSIBILITY_AREAS.md)** - Áreas de responsabilidade

---

## 🚀 QUICK START

### Para Desenvolvedores
1. Leia [FLOW_OPEN_ORDER.md](flows/FLOW_OPEN_ORDER.md)
2. Leia [DATABASE_SECURITY.md](security/DATABASE_SECURITY.md)
3. Execute testes em [AUDIT_ORDER_FLOW.md](AUDIT_ORDER_FLOW.md)

### Para Testadores (QA)
1. Leia [AUDIT_ORDER_FLOW.md](AUDIT_ORDER_FLOW.md)
2. Execute checklists sequencialmente
3. Documente resultados

### Para Gestores
1. Leia [RELEASE_v1.0.md](RELEASE_v1.0.md)
2. Consulte [DELEGATION_PLAN.md](DELEGATION_PLAN.md)

---

## 🆘 Troubleshooting

| Problema | Documento |
|----------|-----------|
| Ordens não copiam | [FLOW_OPEN_ORDER.md](flows/FLOW_OPEN_ORDER.md) - Seção "Possíveis Erros" |
| Erro 500 ao salvar | [CHECK_SERVER_VERSION.md](CHECK_SERVER_VERSION.md) |
| Banco de dados | [DATABASE_OFFICIAL.md](DATABASE_OFFICIAL.md) |
| Segurança | [DATABASE_SECURITY.md](security/DATABASE_SECURITY.md) |

---

**Mantido por:** Equipe Zulfinance  
**Contato:** Issues no GitHub
