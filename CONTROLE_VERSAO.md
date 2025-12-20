# 📦 Controle de Versão com Git

## 🎯 O que é Controle de Versão?

Controle de versão (Git) permite:
- ✅ Salvar histórico de mudanças
- ✅ Voltar para versões anteriores
- ✅ Trabalhar em equipe
- ✅ Fazer backup do código
- ✅ Criar branches para testar novas funcionalidades

---

## 🚀 PASSO 1: Instalar Git (Se não tiver)

### Verificar se já tem Git

```bash
git --version
```

Se aparecer uma versão (ex: `git version 2.40.0`), já está instalado!

### Se não tiver Git instalado:

1. **Baixar Git:**
   - Acesse: https://git-scm.com/download/win
   - Baixe a versão para Windows

2. **Instalar:**
   - Execute o instalador
   - Clique "Next" em todas as telas (configurações padrão são boas)
   - Marque "Add Git to PATH" se aparecer opção
   - Clique "Install"

3. **Verificar instalação:**
   ```bash
   git --version
   ```

---

## 🔧 PASSO 2: Configurar Git (Primeira Vez)

### Configurar seu nome e email

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

**Exemplo:**
```bash
git config --global user.name "Jose Mejia"
git config --global user.email "josemejia@exemplo.com"
```

### Verificar configuração

```bash
git config --list
```

---

## 📁 PASSO 3: Inicializar Repositório Git no Projeto

### 3.1 Ir para pasta do projeto

```bash
cd C:\Users\josemejia\dev\python\aibot
```

### 3.2 Inicializar Git

```bash
git init
```

**✅ Sucesso:** Você verá `Initialized empty Git repository`

### 3.3 Verificar status

```bash
git status
```

Mostra todos os arquivos que ainda não foram adicionados ao Git.

---

## 💾 PASSO 4: Primeiro Commit (Salvar Versão)

### 4.1 Adicionar todos os arquivos

```bash
git add .
```

Isso adiciona todos os arquivos ao "stage" (prontos para commit).

### 4.2 Fazer primeiro commit

```bash
git commit -m "Initial commit: AI Trading Bot MVP"
```

**✅ Sucesso:** Você verá mensagem de commit criado

### 4.3 Verificar histórico

```bash
git log
```

Mostra todos os commits feitos.

---

## 🔄 PASSO 5: Trabalho Diário com Git

### Fluxo Básico

```bash
# 1. Ver o que mudou
git status

# 2. Adicionar arquivos modificados
git add .

# 3. Fazer commit (salvar versão)
git commit -m "Descrição do que foi feito"

# 4. Ver histórico
git log
```

### Exemplos de Commits

```bash
# Adicionar nova funcionalidade
git add .
git commit -m "feat: adiciona painel de estatísticas"

# Corrigir bug
git add .
git commit -m "fix: corrige erro de conexão MT5"

# Atualizar documentação
git add .
git commit -m "docs: atualiza guia de instalação"

# Melhorar código
git add .
git commit -m "refactor: melhora estrutura do código"
```

---

## 🌿 PASSO 6: Criar Branches (Versões Paralelas)

### Criar nova branch

```bash
# Criar e mudar para nova branch
git checkout -b nome-da-branch

# Exemplo: criar branch para testar nova funcionalidade
git checkout -b feature/nova-funcionalidade
```

### Ver em qual branch está

```bash
git branch
```

O branch atual aparece com `*`

### Voltar para branch principal

```bash
git checkout main
# ou
git checkout master
```

### Mesclar branch

```bash
# Ir para branch principal
git checkout main

# Mesclar branch
git merge nome-da-branch
```

---

## 📤 PASSO 7: Usar GitHub/GitLab (Opcional)

### 7.1 Criar repositório no GitHub

1. Acesse: https://github.com
2. Faça login ou crie conta
3. Clique em "New repository"
4. Dê um nome (ex: `ai-trading-bot`)
5. **NÃO** marque "Initialize with README"
6. Clique "Create repository"

### 7.2 Conectar projeto local ao GitHub

```bash
# Adicionar repositório remoto
git remote add origin https://github.com/seu-usuario/ai-trading-bot.git

# Verificar
git remote -v
```

### 7.3 Enviar código para GitHub

```bash
# Primeira vez (criar branch main)
git branch -M main

# Enviar código
git push -u origin main
```

### 7.4 Atualizar GitHub após mudanças

```bash
# Adicionar mudanças
git add .

# Fazer commit
git commit -m "Descrição das mudanças"

# Enviar para GitHub
git push
```

---

## 🔍 Comandos Úteis do Git

### Ver diferenças

```bash
# Ver o que mudou nos arquivos
git diff

# Ver diferenças de um arquivo específico
git diff arquivo.py
```

### Ver histórico

```bash
# Ver commits
git log

# Ver histórico resumido
git log --oneline

# Ver histórico com gráfico
git log --graph --oneline --all
```

### Desfazer mudanças

```bash
# Desfazer mudanças em arquivo não commitado
git checkout -- arquivo.py

# Desfazer último commit (mantém arquivos)
git reset --soft HEAD~1

# Ver mudanças antes de desfazer
git diff HEAD
```

### Ver informações

```bash
# Ver status
git status

# Ver configuração
git config --list

# Ver branches
git branch

# Ver repositórios remotos
git remote -v
```

---

## 📋 Convenções de Commits (Boas Práticas)

Use prefixos para organizar commits:

```bash
# Nova funcionalidade
git commit -m "feat: adiciona sistema de notificações"

# Correção de bug
git commit -m "fix: corrige cálculo de lucro"

# Documentação
git commit -m "docs: atualiza README"

# Melhoria de código
git commit -m "refactor: reorganiza estrutura de pastas"

# Testes
git commit -m "test: adiciona testes para IA"

# Estilo/formatação
git commit -m "style: formata código com black"

# Performance
git commit -m "perf: otimiza consultas ao banco"
```

---

## 🎯 Workflow Recomendado

### Para Desenvolvimento Diário

```bash
# 1. Ver o que mudou
git status

# 2. Adicionar mudanças
git add .

# 3. Fazer commit com mensagem descritiva
git commit -m "feat: adiciona nova funcionalidade X"

# 4. Se usar GitHub, enviar
git push
```

### Para Nova Funcionalidade

```bash
# 1. Criar branch
git checkout -b feature/nome-funcionalidade

# 2. Trabalhar na funcionalidade
# ... fazer mudanças ...

# 3. Commitar
git add .
git commit -m "feat: implementa funcionalidade X"

# 4. Voltar para main e mesclar
git checkout main
git merge feature/nome-funcionalidade

# 5. Deletar branch (opcional)
git branch -d feature/nome-funcionalidade
```

---

## 🔒 Arquivos Ignorados

O arquivo `.gitignore` já está configurado para ignorar:
- `node_modules/` (dependências do frontend)
- `venv/` (ambiente virtual Python)
- `data/` (banco de dados e dados sensíveis)
- `*.pyc` (arquivos compilados Python)
- `.env` (variáveis de ambiente)

**Não precisa fazer nada, já está configurado!**

---

## ✅ Checklist de Configuração

- [ ] Git instalado (`git --version`)
- [ ] Nome e email configurados
- [ ] Repositório inicializado (`git init`)
- [ ] Primeiro commit feito
- [ ] `.gitignore` verificado
- [ ] (Opcional) GitHub configurado

---

## 🚀 Comandos Rápidos (Resumo)

```bash
# Configurar (primeira vez)
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Inicializar projeto
git init
git add .
git commit -m "Initial commit"

# Trabalho diário
git add .
git commit -m "Descrição"
git push  # Se usar GitHub

# Ver informações
git status
git log
git branch
```

---

## 📚 Recursos Adicionais

- **Documentação Git:** https://git-scm.com/doc
- **GitHub Guides:** https://guides.github.com
- **Git Cheat Sheet:** https://education.github.com/git-cheat-sheet-education.pdf

---

## 🆘 Problemas Comuns

### Erro: "fatal: not a git repository"

**Solução:** Execute `git init` na pasta do projeto

### Erro: "Please tell me who you are"

**Solução:** Configure nome e email:
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

### Erro ao fazer push para GitHub

**Solução:** Verifique se o repositório remoto está configurado:
```bash
git remote -v
```

---

## 🎉 Pronto!

Agora você tem controle de versão configurado! Use `git commit` regularmente para salvar seu progresso.

