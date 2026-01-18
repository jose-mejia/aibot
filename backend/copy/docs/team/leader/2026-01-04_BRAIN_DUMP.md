# 🧠 CORE BRAIN DUMP - Data: 2026-01-04
**Entidade:** Antigravity (Tech Lead AI)
**Fase:** Estabilização Crítica (Hotfix Conexão MT5)

---

## 🧐 Estado Mental Atual
Minha função inverteu de "Codificador" para **"Líder Técnico e Gatekeeper"**.
Não estou mais focado em escrever features, mas em garantir integridade, processos e validar soluções de outros devs.
Modo de operação: **Supervisão e Documentação Exaustiva**.

## 💡 Aprendizados do Dia (Knowledge Graph)
1.  **O "Fantasma" do Build Tauri:**
    - *Descoberta:* `npm run tauri build` NÃO atualiza o binário Python (`sidecar`) se ele já existir na pasta `target` ou `binaries`. Ele usa um cache antigo.
    - *Solução:* É OBRIGATÓRIO deletar o binário velho ou compilar manualmente via `pyinstaller` antes de rodar o build do Tauri.
    - *Impacto:* Isso explica por que correções no código Python não apareciam em produção.

2.  **Infraestrutura de Documentação:**
    - Criamos um "Sistema Operacional de Equipe" em `docs/team/`.
    - Definimos personas (`PROMPT_*.md`) para escalar o time. Isso permite que qualquer dev saiba exatamente o que fazer sem microgerenciamento.

## ⚠️ Contexto Imutável (Não Esquecer)
- **Tauri + Python:** O acoplamento é via STDIN/STDOUT. Se o Python quebrar silenciosamente, a GUI fica cega. Logs são vitais.
- **Git Flow:** NENHUM código sobe para a `main` sem aprovação minha.
- **Banco de Dados:** O `aibot.db` é a fonte da verdade. Scripts de migração devem ser tratados com extremo cuidado.

## 🎯 Foco Tático (Próximas Horas)
1.  Validar se o build manual do Client Copier funcionou.
2.  Testar o fluxo ponta-a-ponta (Master -> API -> Client).
3.  Commitar e limpar a bagunça do Git (arquivos soltos).
