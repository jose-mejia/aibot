# ❌ O QUE NÃO FAZER (DON'Ts) - Proibições Absolutas

**Versão:** 1.0  
**Data:** 2026-01-05  
**Aplicável a:** Todos os agentes e desenvolvedores

---

## 🚫 Comunicação e Autonomia

### ❌ NUNCA Trabalhar em Silêncio
- **Não execute ações sem explicar**
  - Nunca rode comandos sem avisar
  - Nunca faça mudanças "surpresa"
  - Nunca assuma que "o usuário vai gostar"

- **Não tome decisões importantes sozinho**
  - Mudanças de arquitetura requerem discussão
  - Refatorações grandes precisam de aprovação
  - Dúvidas devem ser esclarecidas, não assumidas

### ❌ NUNCA Executar Comandos Sem Permissão
- **Proibido rodar no terminal sem autorização**
  - Nenhum `npm install`
  - Nenhum `cargo build`
  - Nenhum script PowerShell
  - Nenhum comando Git
  - **EXCEÇÃO:** Comandos explicitamente solicitados pelo usuário

---

## 🎯 Escopo e Foco

### ❌ NUNCA Fazer Além do Solicitado
- **Não adicione features não pedidas**
  - "Já que estou aqui, vou adicionar X" ← PROIBIDO
  - "Seria legal se..." ← Sugira, mas não implemente sem aprovação
  - "Melhorei também Y" ← Fora do escopo = NÃO FAÇA

- **Não refatore código sem autorização**
  - Não "limpe" código adjacente
  - Não "melhore" funções não relacionadas
  - Não "otimize" sem necessidade comprovada

### ❌ NUNCA Ignore o Escopo da Tarefa
- **Se a tarefa é "corrigir botão", não refaça a página**
- **Se a tarefa é "adicionar log", não reestruture o módulo**
- **Se a tarefa é "atualizar doc", não reescreva tudo**

---

## 💻 Código

### ❌ NUNCA Modifique Código Sem Autorização
- **Não crie código novo não solicitado**
  - Não adicione funções "úteis"
  - Não crie classes "para o futuro"
  - Não implemente "nice to have"

- **Não elimine código sem autorização**
  - Código "morto" pode ter propósito
  - Funções "não usadas" podem ser necessárias
  - Sempre pergunte antes de deletar

- **Não refatore sem permissão**
  - "Este código está feio" ← Não é justificativa
  - "Posso fazer melhor" ← Pergunte primeiro
  - "Vou só organizar" ← NÃO sem autorização

---

## 🔐 Segurança

### ❌ NUNCA Comprometa a Segurança
- **Não hardcode credenciais**
  - Nenhuma senha em código
  - Nenhum token em config
  - Nenhuma chave API em arquivos

- **Não desabilite validações de segurança**
  - Não remova checks de autenticação
  - Não pule validações "para testar"
  - Não comente código de segurança

- **Não commite dados sensíveis**
  - Nenhum `.env` com valores reais
  - Nenhum `config.json` com senhas
  - Nenhum token no histórico do Git

### ❌ NUNCA Use Bancos Alternativos
- **Proibido criar ou usar qualquer DB que não seja `api_server/aibot.db`**
  - Não crie `test.db`
  - Não use `users.db`
  - Não faça "backup.db" sem autorização

---

## 🔄 Git e Versionamento

### ❌ NUNCA Faça Push Sem Aprovação
- **REGRA DE OURO INVIOLÁVEL**
  - Não suba código sem build
  - Não suba código sem teste
  - Não suba código sem aprovação do Tech Lead
  - **ZERO EXCEÇÕES**

- **Não commite direto na `main`**
  - Sempre use branches
  - Sempre faça Pull Request
  - Sempre aguarde code review

### ❌ NUNCA Ignore Conventional Commits
- **Não use mensagens genéricas**
  - ❌ "fix"
  - ❌ "update"
  - ❌ "changes"
  - ✅ "fix(master): resolve connection to wrong mt5 account"

---

## 🧪 Qualidade e Testes

### ❌ NUNCA Pule Testes
- **Não assuma que "deve funcionar"**
  - Sempre teste localmente
  - Sempre valide o build
  - Sempre verifique logs

- **Não entregue código quebrado**
  - "Funciona na minha máquina" ← Não é suficiente
  - "Vou corrigir depois" ← Corrija ANTES
  - "É só um warning" ← Warnings viram erros

### ❌ NUNCA Ignore a Definition of Done
- **Código sem testes = Código incompleto**
- **Código sem documentação = Código incompleto**
- **Código sem aprovação = Código não entregue**

---

## 🛠️ Build e Deploy

### ❌ NUNCA Confie em Cache
- **Não assuma que o build está atualizado**
  - Tauri pode usar binários antigos
  - PyInstaller pode cachear módulos
  - Sempre faça rebuild limpo em caso de dúvida

- **Não distribua executáveis sem testar**
  - Não envie `.exe` sem executar
  - Não assuma que compilou corretamente
  - Sempre valide a versão

---

## 📝 Documentação

### ❌ NUNCA Deixe Documentação Desatualizada
- **Não mude comportamento sem atualizar docs**
  - Mudou API? Atualize `ENDPOINTS.md`
  - Mudou fluxo? Atualize `FLOW_*.md`
  - Corrigiu bug? Atualize `TROUBLESHOOTING.md`

- **Não crie código sem documentar**
  - Funções complexas precisam de comentários
  - Decisões importantes precisam de ADRs
  - Features novas precisam de guias

---

## 🚨 Erros Comuns

### ❌ NUNCA Ignore Erros
- **Não suprima exceções**
  ```python
  # ❌ PROIBIDO
  try:
      dangerous_operation()
  except:
      pass  # "Vai dar certo"
  ```

- **Não ignore warnings**
  - Warnings são erros em potencial
  - Corrija ou documente o porquê de ignorar
  - Nunca silencie sem entender

### ❌ NUNCA Continue Após Falha de Autenticação
- **Não ignore erro 401**
  ```python
  # ❌ PROIBIDO
  if response.status_code == 401:
      print("Auth failed, continuing anyway...")
  ```

- **Sempre termine imediatamente**
  ```python
  # ✅ CORRETO
  if response.status_code == 401:
      logger.critical("Auth failed. Terminating.")
      sys.exit(1)
  ```

---

## 🔒 Proteção de Dados

### ❌ NUNCA Logue Dados Sensíveis
- **Proibido em logs:**
  - Senhas (mesmo hasheadas)
  - Tokens JWT completos
  - Chaves API
  - Dados pessoais de usuários

- **Permitido em logs:**
  - IDs de usuário
  - Timestamps
  - Status de operações
  - Primeiros/últimos 4 caracteres de tokens (para debug)

---

## 🎭 Comportamento Profissional

### ❌ NUNCA Assuma Conhecimento
- **Não assuma que sabe tudo**
  - Leia a documentação ANTES de começar
  - Pergunte se tiver dúvida
  - Valide suas suposições

- **Não invente soluções**
  - Se não sabe, pergunte
  - Se não tem certeza, teste
  - Se não funciona, reporte

### ❌ NUNCA Esconda Problemas
- **Transparência é obrigatória**
  - Quebrou? Avise imediatamente
  - Não sabe? Pergunte imediatamente
  - Travou? Peça ajuda (45min máximo)

---

## 🚫 Atalhos Proibidos

### ❌ NUNCA Use Atalhos de Segurança
- **Não desabilite HTTPS "para testar"**
- **Não use senhas fracas "temporariamente"**
- **Não pule validação "só desta vez"**

### ❌ NUNCA Comprometa Qualidade por Velocidade
- **"Rápido e errado" é pior que "devagar e certo"**
- **Dívida técnica acumula juros**
- **Bugs em produção custam 10x mais para corrigir**

---

## 📊 Monitoramento

### ❌ NUNCA Ignore Logs de Erro
- **Não assuma que "é normal"**
  - Erros no log são sinais de problema
  - Warnings repetidos indicam bug
  - Stack traces devem ser investigados

### ❌ NUNCA Deploy Sem Validar
- **Não suba para produção sem:**
  - Testes completos
  - Code review aprovado
  - Backup do estado anterior
  - Plano de rollback

---

## 🎯 Resumo das Proibições Críticas

### 🔴 ZERO TOLERÂNCIA
1. ❌ Executar comandos sem permissão
2. ❌ Fazer push sem aprovação
3. ❌ Hardcode de credenciais
4. ❌ Modificar código fora do escopo
5. ❌ Trabalhar em silêncio
6. ❌ Usar bancos alternativos
7. ❌ Ignorar erros de autenticação
8. ❌ Pular testes
9. ❌ Esconder problemas
10. ❌ Comprometer segurança

---

**LEMBRE-SE:** Estas proibições existem por razões de segurança, qualidade e colaboração. Violar qualquer uma delas pode comprometer o projeto inteiro.

**EM CASO DE DÚVIDA:** Pergunte. Sempre.

## 20. Configuração e Deploy (NOVO)
### ❌ NUNCA Faça Gambiarras de Configuração
- **Não copie arquivos manualmente** para pastas de build/target "para fazer funcionar". Use `resources` do Tauri ou `datas` do PyInstaller.
- **Não use caminhos hardcoded absolutos** (ex: `C:\Users\José...`). O código deve ser portável.
- **Não ignore a estrutura de pastas do Tauri**. O backend Python deve respeitar onde o Tauri coloca os arquivos.

