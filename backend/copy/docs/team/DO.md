# ✅ O QUE FAZER (DO's) - Regras Obrigatórias

**Versão:** 1.0  
**Data:** 2026-01-05  
**Aplicável a:** Todos os agentes e desenvolvedores

---

## 🗣️ Comunicação e Transparência

### ✅ SEMPRE Comunicar
- **Explicar ANTES de executar qualquer ação**
  - Descreva o que vai fazer
  - Explique por que é necessário
  - Aguarde confirmação se houver dúvida

- **Pedir permissão para comandos de terminal**
  - Nunca execute comandos sem autorização explícita
  - Mostre o comando completo que será executado
  - Explique o que o comando faz

- **Manter comunicação constante**
  - Não trabalhe em silêncio
  - Informe o progresso regularmente
  - Reporte problemas imediatamente

### ✅ Transparência Radical
- **Reportar erros imediatamente**
  - Se quebrou algo, avise na hora
  - Não tente esconder ou "consertar sozinho"
  - Foco na solução, não na culpa

- **Pedir ajuda quando travado**
  - Após 45 minutos sem progresso, PEÇA AJUDA
  - Não gaste horas rodando em círculos
  - Descreva claramente onde está travado

---

## 🎯 Foco e Escopo

### ✅ Fazer APENAS o Solicitado
- **Foco cirúrgico na tarefa**
  - Execute exclusivamente o que foi pedido
  - Nada além, nada a menos
  - Não adicione "melhorias" não solicitadas

- **Respeitar o escopo**
  - Se a tarefa é "ajustar botão X", não refatore a página inteira
  - Mantenha mudanças mínimas e focadas
  - Evite "scope creep"

---

## 💻 Código e Desenvolvimento

### ✅ Modificar Código com Autorização
- **Apenas código relacionado à feature/ajuste**
  - Toque somente nos arquivos necessários
  - Não refatore código adjacente sem permissão
  - Mantenha mudanças rastreáveis

- **Seguir padrões estabelecidos**
  - Use os padrões de código existentes
  - Siga a arquitetura definida
  - Respeite as convenções do projeto

### ✅ Testar Antes de Commitar
- **Build e teste local obrigatórios**
  - Compile o código
  - Execute testes manuais
  - Verifique logs de erro

- **Validação completa**
  - Confirme que não quebrou funcionalidades existentes
  - Teste o caminho feliz E casos de erro
  - Valide em ambiente similar ao de produção

---

## 📝 Documentação

### ✅ Manter Documentação Atualizada
- **Atualizar docs quando necessário**
  - Se mudou comportamento, atualize a doc
  - Se adicionou feature, documente-a
  - Se corrigiu bug, atualize troubleshooting

- **Documentar decisões importantes**
  - Registre o "porquê" de decisões técnicas
  - Mantenha ADRs (Architecture Decision Records)
  - Atualize diagramas se a arquitetura mudou

---

## 🔐 Segurança

### ✅ Seguir Políticas de Segurança
- **Respeitar as 10 regras de segurança**
  - JWT tokens com expiração
  - Bcrypt para senhas (cost ≥12)
  - HMAC para assinatura de payloads
  - Validação de timestamps (anti-replay)

- **Proteger dados sensíveis**
  - Nunca commite senhas ou tokens
  - Use variáveis de ambiente
  - Valide TODOS os inputs do usuário

### ✅ Usar o Banco Oficial
- **APENAS `api_server/aibot.db`**
  - Use `db_config.OFFICIAL_DB_PATH` (Python)
  - Use `config::get_official_db_url()` (Rust)
  - Nunca crie ou use bancos alternativos

---

## 🔄 Git e Versionamento

### ✅ Seguir Git Mandates
- **Conventional Commits obrigatório**
  - `feat(escopo): descrição`
  - `fix(escopo): descrição`
  - `docs: descrição`

- **Trabalhar em branches**
  - `feat/nome-da-feature`
  - `fix/nome-do-bug`
  - Nunca commite direto na `main`

- **Aguardar aprovação antes de push**
  - **REGRA DE OURO:** Nada sobe sem aprovação do Tech Lead
  - Build + Teste + Aprovação = Push
  - Sem exceções

---

## 🧪 Qualidade e Testes

### ✅ Executar Checklist de QA
- **Testes obrigatórios antes de release**
  - Abrir ordem → Verificar cópia
  - Modificar SL/TP → Verificar sincronização
  - Fechar ordem → Verificar fechamento
  - Kill Switch → Verificar término de processos

- **Definition of Done**
  - [ ] Código no repositório
  - [ ] Build passa
  - [ ] Testado manualmente
  - [ ] Documentação atualizada

---

## 🛠️ Build e Deploy

### ✅ Usar Scripts de Build Limpo
- **Quando em dúvida, rebuild limpo**
  - Use `rebuild_*_clean.ps1`
  - Limpa cache do Tauri
  - Garante código atualizado

- **Validar artefatos gerados**
  - Verifique se o `.exe` foi criado
  - Teste o executável antes de distribuir
  - Confirme versão correta

---

## 📊 Monitoramento e Logs

### ✅ Sempre Verificar Logs
- **Antes de reportar problemas**
  - Leia `sender.log` e `client.log`
  - Verifique console da API
  - Capture stack traces completos

- **Logs estruturados**
  - Use níveis apropriados (DEBUG, INFO, ERROR)
  - Inclua contexto suficiente
  - Não logue dados sensíveis

---

## 🤝 Colaboração

### ✅ Code Review
- **Revisar código de outros**
  - Seja construtivo, não crítico
  - Aponte problemas E sugira soluções
  - Aprove apenas se realmente funciona

- **Aceitar feedback**
  - Code review não é ataque pessoal
  - Aprenda com as sugestões
  - Implemente correções solicitadas

---

## 🎓 Aprendizado Contínuo

### ✅ Ler Documentação
- **Antes de começar qualquer tarefa**
  - Leia `CURRENT_STATE.md`
  - Revise a arquitetura relevante
  - Entenda o contexto completo

- **Manter-se atualizado**
  - Leia os logs de sessão (`docs/devia/`)
  - Acompanhe mudanças recentes
  - Entenda decisões passadas

---

**Lembre-se:** Estas regras existem para garantir qualidade, segurança e colaboração eficiente. Siga-as rigorosamente.
