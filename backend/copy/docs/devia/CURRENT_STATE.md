# 🧠 ESTADO ATUAL DO PROJETO (Consciência da IA)
**Última Atualização:** 04/01/2026
**Contexto:** Pós-Hotfix de Conexão MT5

---

## 📍 Onde Estamos?
O sistema está em fase de **Validação Final (End-to-End)**.
Acabamos de resolver um bloqueio crítico onde o Master Sender conectava na conta errada.

### ✅ O que está FUNCIONANDO:
1.  **Backend Rust (API):**
    - Autenticação JWT OK.
    - Banco de Dados Unificado (`aibot.db`) OK.
    - Endpoints de Configuração de Usuário (`mt5_path`) OK.

2.  **Master Sender (Python + Tauri):**
    - **Correção Aplicada:** O binário Python foi recompilado manualmente para incluir a lógica que lê o `mt5_path` do banco.
    - **Status:** Build finalizado com sucesso. Deve conectar no ID `7409735`.
    - **Lógica:** Detecta TODAS as ordens (manuais e robôs).

3.  **Client Copier (Python + Tauri):**
    - **Status:** Rebuild realizado/pendente para garantir simetria com o Master.
    - **Lógica:** Recebe sinais via WebSocket e executa com arredondamento de preço corrigido.

---

## 🏗️ Arquitetura Resumida
- **Core:** Rust API (Porta 8000) controla tudo. É a única que toca no Banco.
- **Sidecars:** Scripts Python que rodam "dentro" do Tauri (Interface Gráfica).
- **Comunicação:** Tauri <-> Python via Stdin/Stdout. Python <-> API via HTTP/WebSocket.
- **Persistência:** SQLite (`aibot.db`).

---

## ⚠️ Pontos de Atenção (Handover)
Se você acabou de chegar no projeto, CUIDADO com:
1.  **Build do Tauri:** Se alterar o Python (`.py`), o `npm run tauri build` **NÃO** atualiza o `.exe` do Python automaticamente se ele já existir na pasta `binaries`.
    - **Solução:** Use os scripts `scripts/build/rebuild_*.ps1` ou delete o `.exe` antigo manualmente antes do build.
2.  **Caminhos MT5:** O sistema depende estritamente que o `mt5_path` no banco de dados aponte para o `terminal64.exe` correto de cada conta.

## 📝 Histórico Recente
- **04/01:** Debug do `mt5_path` ignorado. Solução via PyInstaller manual.
- **03/01:** Unificação dos bancos de dados e limpeza de scripts raiz.

---

## 📂 Mapa da Documentação
- `docs/database/`: Esquema das tabelas.
- `docs/flows/`: Diagramas de como as ordens são copiadas.
- `docs/devia/`: Logs detalhados de sessões anteriores.
