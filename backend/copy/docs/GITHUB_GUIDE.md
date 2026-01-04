# 📘 Guia Prático de GitHub para Gerenciar o Projeto Zulfinance

**Para:** Jose Mejia (Product Owner)  
**Nível:** Iniciante/Intermediário  
**Objetivo:** Gerenciar tarefas, revisar código e acompanhar progresso sem ser expert em Git

---

## 🎯 O que é GitHub e Por Que Usamos?

**GitHub = Rede Social para Código**

Imagine o GitHub como:
- **Google Drive** (armazena código na nuvem)
- **Trello** (organiza tarefas em Issues)
- **WhatsApp** (discussões sobre o código)

### **O que NÃO precisamos fazer (deixa comigo):**
- ❌ Comandos avançados de Git
- ❌ Resolver conflitos de merge
- ❌ Configurar CI/CD

### **O que VOCÊ vai fazer (simples):**
- ✅ Criar tarefas (Issues)
- ✅ Acompanhar progresso
- ✅ Aprovar ou rejeitar código (Pull Requests)
- ✅ Ver histórico de mudanças

---

## 📋 Parte 1: Issues (Tarefas)

### **O que é uma Issue?**
É como um **cartão do Trello** ou **ticket de suporte**. Cada Issue representa uma tarefa.

### **Como Criar uma Issue (Passo a Passo):**

1. **Vá para o repositório no GitHub:**
   - Exemplo: https://github.com/jose-mejia/client_copier

2. **Clique na aba "Issues"** (no menu superior)

3. **Clique no botão verde "New Issue"**

4. **Preencha os campos:**
   ```
   Título: [FRONTEND] Criar página de histórico de trades
   
   Descrição:
   ## Objetivo
   Criar uma nova página que mostre todas as ordens copiadas.
   
   ## Critérios de Aceitação
   - [ ] Tabela com colunas: Data, Símbolo, Tipo, Lote, SL, TP
   - [ ] Filtro por data (últimos 7 dias, 30 dias, etc.)
   - [ ] Paginação (10 trades por página)
   
   ## Arquivos Afetados
   - `gui/src/pages/TradeHistory.tsx` (criar novo)
   - `gui/src/Router.tsx` (adicionar rota)
   
   ## Prioridade
   - [x] Alta
   - [ ] Média
   - [ ] Baixa
   ```

5. **Adicione Labels (etiquetas):**
   - `frontend` (área)
   - `enhancement` (tipo)
   - `high priority` (prioridade)

6. **Atribua para alguém:**
   - Se for você mesmo: Assign to yourself
   - Se for um dev: Escolha o nome dele

7. **Clique em "Submit new issue"**

### **Como Acompanhar Issues:**

**Visualização em Lista:**
- Abra a aba "Issues"
- Veja todas as tarefas abertas
- Filtre por label: `label:frontend` ou `label:security`

**Visualização em Board (Kanban):**
1. Vá em "Projects" (no menu superior)
2. Crie um novo Project: "Zulfinance Development"
3. Escolha template: "Board"
4. Arraste Issues entre colunas:
   - **To Do** (A fazer)
   - **In Progress** (Em andamento)
   - **Review** (Em revisão)
   - **Done** (Concluído)

---

## 🔀 Parte 2: Pull Requests (Revisão de Código)

### **O que é um Pull Request (PR)?**
É quando um dev diz: **"Terminei a tarefa, pode revisar?"**

### **Como Revisar um Pull Request (Passo a Passo):**

1. **Você recebe notificação:**
   - Email: "Dev X opened a pull request"
   - Ou vá em: https://github.com/jose-mejia/client_copier/pulls

2. **Clique no Pull Request** para abrir

3. **Veja o que mudou:**
   - Aba "Files changed" mostra o código modificado
   - Linhas verdes = código adicionado
   - Linhas vermelhas = código removido

4. **Teste localmente (Opcional mas recomendado):**
   ```bash
   # No terminal, dentro da pasta do projeto:
   git fetch origin
   git checkout nome-da-branch
   npm run dev  # Ou o comando para rodar o projeto
   ```

5. **Deixe um comentário:**
   - Se está bom: "LGTM! ✅" (Looks Good To Me)
   - Se tem problema: "Por favor, ajuste X e Y"

6. **Aprove ou Rejeite:**
   - Botão "Review changes" (canto superior direito)
   - Escolha:
     - **Approve** (Aprovar) ✅
     - **Request changes** (Pedir mudanças) 🔄
     - **Comment** (Apenas comentar) 💬

7. **Merge (Se aprovado):**
   - Botão verde "Merge pull request"
   - Confirme: "Confirm merge"
   - Delete a branch (opcional): "Delete branch"

### **Exemplo de Fluxo Completo:**

```
1. Dev cria Issue: "Adicionar botão de logout"
2. Dev cria branch: feature/logout-button
3. Dev faz mudanças no código
4. Dev abre Pull Request: "feat: Add logout button"
5. Você revisa o código
6. Você testa localmente (opcional)
7. Você aprova: "LGTM! ✅"
8. Você faz merge
9. Issue é fechada automaticamente
```

---

## 📊 Parte 3: Acompanhar Progresso

### **Dashboard Simples (Insights):**

1. **Vá para o repositório**
2. **Clique em "Insights"** (menu superior)
3. **Veja:**
   - **Pulse:** Atividade da última semana
   - **Contributors:** Quem está contribuindo mais
   - **Commits:** Histórico de mudanças

### **Ver Histórico de Mudanças:**

1. **Vá para a aba "Commits"**
2. **Veja lista de commits:**
   ```
   feat: Add logout button (por Dev X, há 2 horas)
   fix: Corrigir bug no login (por Dev Y, ontem)
   docs: Atualizar README (por Antigravity, há 3 dias)
   ```

3. **Clique em um commit** para ver o que mudou

---

## 🏷️ Parte 4: Labels (Etiquetas)

### **Labels Recomendadas:**

**Por Área:**
- `frontend` 🎨 (Tudo relacionado a UI)
- `security` 🔒 (Tudo relacionado a segurança)
- `architecture` 🏗️ (Tudo relacionado a arquitetura)
- `backend` ⚙️ (API Rust)
- `python` 🐍 (Sidecars Python)

**Por Tipo:**
- `bug` 🐛 (Algo está quebrado)
- `enhancement` ✨ (Nova feature)
- `documentation` 📝 (Atualizar docs)
- `refactor` 🔧 (Melhorar código existente)

**Por Prioridade:**
- `high priority` 🔴 (Urgente)
- `medium priority` 🟡 (Importante)
- `low priority` 🟢 (Pode esperar)

### **Como Criar Labels:**

1. Vá em "Issues"
2. Clique em "Labels"
3. Clique em "New label"
4. Preencha:
   - Name: `frontend`
   - Description: `Tudo relacionado a UI/UX`
   - Color: Escolha uma cor (ex: azul)
5. Clique em "Create label"

---

## 🔔 Parte 5: Notificações

### **Como Configurar Notificações:**

1. **Vá em Settings (do repositório)**
2. **Clique em "Notifications"**
3. **Escolha:**
   - **Watch:** Receber notificação de TUDO (não recomendado)
   - **Participating:** Receber apenas quando mencionado ou envolvido
   - **Ignore:** Não receber nada

**Recomendação:** Use "Participating" para não ficar sobrecarregado.

### **Como Ver Notificações:**

1. **Ícone de sino** (canto superior direito do GitHub)
2. **Veja lista de notificações:**
   - "Dev X mentioned you in #42"
   - "Pull Request #15 was merged"

---

## 🎯 Parte 6: Workflow Diário (Seu Papel)

### **Manhã (10 minutos):**
1. Abra GitHub
2. Vá em "Issues"
3. Veja o que está em "In Progress"
4. Veja se há Pull Requests esperando revisão

### **Tarde (15 minutos):**
1. Revise Pull Requests abertos
2. Teste localmente (se possível)
3. Aprove ou peça mudanças

### **Fim do Dia (5 minutos):**
1. Veja "Insights" → "Pulse"
2. Veja o que foi feito hoje
3. Planeje tarefas para amanhã

---

## 🆘 Comandos Úteis (Para Você)

### **Ver código de uma branch sem fazer merge:**
```bash
# No terminal, dentro da pasta do projeto:
git fetch origin
git checkout nome-da-branch
npm run dev  # Testar
git checkout main  # Voltar para versão principal
```

### **Ver diferenças entre versões:**
```bash
git diff main..nome-da-branch
```

### **Voltar para versão anterior (se algo quebrar):**
```bash
git log --oneline  # Ver histórico
git reset --hard abc123  # Voltar para commit abc123
```

---

## 📞 Quando Me Chamar (Antigravity)

**Me chame se:**
- ❓ Não entender o que um Pull Request faz
- ❓ Conflito de merge aparecer
- ❓ Precisar desfazer um merge
- ❓ Quiser criar automações (GitHub Actions)

**Não precisa me chamar para:**
- ✅ Criar Issues
- ✅ Aprovar Pull Requests simples
- ✅ Adicionar labels
- ✅ Fechar Issues

---

## 🎓 Recursos de Aprendizado

**Vídeos Curtos (YouTube):**
- "GitHub Issues Tutorial" (5 min)
- "GitHub Pull Requests Explained" (8 min)
- "GitHub Projects Board" (6 min)

**Documentação Oficial:**
- https://docs.github.com/en/issues
- https://docs.github.com/en/pull-requests

---

## ✅ Checklist de Primeiros Passos

- [ ] Criar 3 labels: `frontend`, `security`, `architecture`
- [ ] Criar 1 Issue de teste: "Melhorar README"
- [ ] Criar 1 Project Board: "Zulfinance Development"
- [ ] Configurar notificações para "Participating"
- [ ] Adicionar colaboradores (devs) aos repositórios

---

**Dúvidas? Pergunte! Vou te guiar passo a passo sempre que precisar.** 🚀
