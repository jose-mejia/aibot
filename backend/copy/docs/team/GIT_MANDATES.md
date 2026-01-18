# 🛡️ PROTOCOLO DE GIT E GOVERNANÇA (GIT MANDATES)

**ATENÇÃO:** Todo desenvolvedor neste projeto deve seguir estritamente estas regras. Violações resultarão em reversão imediata de código.

## 1. A Regra de Ouro (Golden Rule)
> **"Nenhum código sobe para o remoto (push) sem antes ter sido testado, buildado e APROVADO explicitamente pelo Tech Lead (User)."**

---

## 2. Padrão de Commits (Conventional Commits)
Nossas mensagens de commit devem ser legíveis por humanos e máquinas.
**Formato:** `tipo(escopo): descrição breve`

### Tipos Permitidos:
- **`feat`**: Nova funcionalidade (ex: `feat(gui): tela de login`).
- **`fix`**: Correção de bug (ex: `fix(core): erro 10015 no mt5`).
- **`docs`**: Apenas documentação (ex: `docs: update readme`).
- **`refactor`**: Mudança de código que não altera funcionalidade (limpeza).
- **`chore`**: Ajustes de build, ferramentas, deps (ex: `chore: update tauri`).
- **`perf`**: Melhoria de performance.

**Exemplo Perfeito:**
`fix(master): resolve connection to wrong mt5 account id`

---

## 3. Estratégia de Branches (GitFlow Simplificado)

1.  **`main` (Sagrada):** O código que está em produção. **NUNCA** commite direto aqui.
2.  **`develop` (Integração):** Onde juntamos as features prontas para teste.
3.  **Feature Branches:** Onde você trabalha.
    - `feat/nome-da-feature`
    - `fix/nome-do-bug`

**Fluxo:**
`feat/login` -> (PR/Merge) -> `develop` -> (Release) -> `main`

---

## 4. Fluxo de Trabalho (Workflow)

### Passo 1: Início
1.  **Sincronize:** Sempre comece com `git pull origin develop`.
2.  **Branch:** Crie sua branch: `git checkout -b feat/minha-feature`.

### Passo 2: Validação (Obrigatória)
Antes de sequer pensar em comitar:
1.  **Build:** O código compila? (`npm run tauri build`, `cargo build`).
2.  **Lint:** O código segue o padrão?
3.  **Teste Manual:** Você rodou o software? Ele abriu? Ele fez o que devia?

### Passo 3: Solicitação de Aprovação
1.  Apresente as mudanças ao Tech Lead.
2.  Mostre os logs de teste ou evidência de funcionamento.
3.  Aguarde o comando: "Pode subir" ou "Aprovado".

## 5. Gestão de Submódulos
Este projeto usa submódulos (`api_server`, `master_sender`, `client_copier`).
- **Cuidado:** Se alterar um submódulo, commite ELE primeiro, depois volte para a raiz e atualize a referência.
- **Não deixe "Detached Head":** Trabalhe sempre em branches dentro dos submódulos também.

---
**Assinatura:** Antigravity (Tech Lead)
