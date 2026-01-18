# 📅 Contexto do Projeto - 04/01/2026
**Autor:** Antigravity (Tech Lead AI)
**Fase:** Estabilização & Hotfix (v1.0 Release Candidate)
**Status:** 🟡 Validando Correções Críticas

---

## 🎯 O Objetivo Imediato
Estamos focados em garantir que o **Master Sender** e o **Client Copier** se conectem estritamente às contas MT5 definidas no banco de dados, sem erros de roteamento (ex: Master conectando na conta do Client).

## 🚧 O Incidente do Dia
Identificamos e corrigimos um bug crítico de build onde o **Tauri** (GUI) estava empacotando uma versão antiga do código Python (`sender-service`), fazendo com que as correções de lógica fossem ignoradas em produção.

**A Solução Aplicada:**
- Implementamos um **Build Manual dos Sidecars** (`scripts/build/rebuild_*.ps1`).
- Forçamos a recompilação do Python via `pyinstaller` antes do empacotamento da GUI.
- **Resultado:** O Master Sender foi reconstruído com sucesso e agora deve carregar o `mt5_path` corretamente do banco de dados.

## 🏗️ Estado da Arquitetura (Visão Macro)
Todo desenvolvedor deve estar ciente da estrutura atual:

1.  **Backend (Rust/Axum):** Operacional na porta `8000`. É a única "Fonte da Verdade" que toca no banco `aibot.db`.
2.  **Database (SQLite):** Unificado em `api_server/aibot.db`. Tabelas principais: `users` (configurações) e `signals` (ordens).
3.  **Frontend (React/Tauri):** Atua apenas como "casca". Inicia os processos Python em background.
4.  **Core (Python):** Scripts que rodam "escondidos" (Sidecars) e falam com o MT5.

## 📜 Governança e Processos (Novo!)
Hoje formalizamos a estrutura de equipe em `docs/team/`. Todos devem ler:
- **`GIT_MANDATES.md`:** Regras de ouro para commits e PRs. Ninguém sobe código na `main` sem teste.
- **`PROMPT_*.md`:** Manuais de função para Backend, Frontend, QA e Core.

## 🔄 Próximos Passos (Backlog Imediato)
1.  **Validação de QA:** Testar se o `Master Sender` conecta no ID `7409735` e o `Client Copier` no ID `11629107`.
2.  **Git Cleanup:** Organizar arquivos soltos gerados durante o hotfix e commitar na branch correta.
3.  **Start v1.0:** Se os testes passarem, congelar a versão `v1.0` para release.

---
*Este arquivo deve ser lido por todos os membros da equipe antes de iniciar o turno de hoje.*
