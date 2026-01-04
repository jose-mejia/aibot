# Dossiê de Continuidade e Diretrizes do Projeto "AIBOT CopyTrading"
**Data:** 03/01/2026
**Autor:** Antigravity (Sessão Anterior)
**Para:** Próximo Agente de IA / Dev Responsável

---

## 🚀 1. Missão Crítica
O objetivo é desenvolver um sistema de CopyTrading (Master -> Client) de **alta performance, latência ultra-baixa e robustez extrema**. O sistema deve ser profissional, seguro e respeitar a soberania do usuário sobre a máquina.

**Filosofia do Projeto ("O Tao do Usuário"):**
*   **Zero Gambiarra**: Soluções devem ser elegantes, estruturadas e definitivas. Nada de hacks temporários.
*   **Soberania do Usuário**: O software é um servo, não um vírus. Ele **NUNCA** deve abrir programas (como o MT5) sem o consentimento explícito e prévio do usuário (via abertura manual).
*   **Cemitério Limpo**: Ao fechar o App Desktop, **TODOS** os processos filho (Python Sidecars) devem morrer instantaneamente. Nenhuma "zombie process" é tolerada.
*   **Segurança de Sessão**: Fechar o App = Logout. Sem persistência perigosa de tokens em máquinas compartilhadas.
*   **UX Premium**: A interface deve reagir instantaneamente (ex: ao trocar o ID do MT5) sem exigir que o usuário pressione F5.

---

## 🏗️ 2. Arquitetura e Estado Atual

### Componentes:
1.  **Master Sender (Python Sidecar)**: Lê ordens do MT5 e envia via HTTP para o servidor.
2.  **API Server (Rust/Axum)**: O cérebro central. Recebe sinais do Master, autentica usuários (JWT), e faz broadcast via WebSocket.
3.  **Client Copier (Python Sidecar)**: Conecta-se ao WebSocket do servidor, recebe sinais e executa no MT5 local.
4.  **Frontend/Desktop Hub (Tauri + React)**: Interface unificada para Master e Client.

### ✅ O que JÁ ESTÁ FUNCIONANDO (Estável):
*   **Fluxo de Ordens**: Master abre ordem -> Rust recebe -> Client via WS recebe -> Client abre ordem no MT5. (Testado e validado hoje).
*   **WebSockets Robustos**: Implementamos `ping_interval=20` e tratamento de erros de JSON para evitar desconexões intermitentes ("pisca-pisca").
*   **Normalização de Dados**: O Client agora aceita tanto `master_ticket`/`type_` quanto `ticket`/`type`, resolvendo conflitos de nomenclatura.
*   **Auto-Recover**: Os sidecars Python possuem loops de retry para conexão inicial com o MT5 (mas vide regra de "Soberania" abaixo).
*   **Atualização Dinâmica de ID**: Ao trocar o MT5 ID na interface, o Python reinicia e conecta na nova conta automaticamente, forçando um refresh na UI.

---

## 📜 3. Diretrizes de Implementação (Regras de Ouro)

O próximo dev DEVE seguir estas regras estritamente:

### A. Regra do "Observador Silencioso" (MT5)
*   **O código Python NÃO PODE usar `mt5.initialize()` cegamente.**
*   **Lógica Obrigatória**: Antes de tentar conectar, o Python deve verificar se o processo `terminal64.exe` já está rodando (usando `tasklist` ou `psutil`).
    *   Se **SIM**: Conecta.
    *   Se **NÃO**: Fica em loop de espera (sleep) e loga "Aguardando usuário abrir MT5". **JAMAIS** invocar o comando de abertura.

### B. Regra do "Kill Switch"
*   O App Tauri (Desktop) é o "pai" dos processos.
*   Ao detectar o evento `tauri://close-requested` ou `window.onunload`:
    1.  O Frontend deve invocar o comando de backend para **MATAR (SIGKILL)** o processo Python Sidecar imediatamente.
    2.  O Frontend deve limpar `sessionStorage` e `localStorage` (Token JWT), garantindo que a reabertura exija novo login.

### C. Estabilidade de Conexão
*   O WebSocket do cliente deve ser tratado como "sagrado". Se cair, deve tentar reconectar indefinidamente (com backoff exponencial), mas sem travar a UI.

---

## 🛠️ 4. Próximos Passos Imediatos (To-Do List)

Você deve começar sua sessão implementando as funcionalidades desenhadas na última conversa:

1.  **Implementar "Modo Observador" no Python**: [FEITO]
    *   Editar `client_copier/mt5_connector.py` e `master_sender/mt5_connector.py`.
    *   Adicionar check de `subprocess` para `terminal64.exe`.
    *   Impedir `mt5.initialize()` se o processo não existir.

2.  **Implementar "Kill Switch & Logout" no Frontend**: [FEITO]
    *   Editar `client_copier/gui/src/App.tsx` e `master_sender/gui/src/App.tsx`.
    *   Adicionar listener para `appWindow.listen("tauri://close-requested", ...)` que chama `stopPythonService()` e limpa tokens.

3.  **Revalidar Build**: [EM ANDAMENTO]
    *   Após as mudanças no Python, rodar `pyinstaller` novamente para gerar novos `.exe`. (Comandos rodando em background)

---

**Nota Final para a IA:** O usuário "Jose" é técnico, exigente e valoriza a transparência. Sempre explique o "porquê" antes do "como". Se for editar código sensível (como loops de conexão), peça confirmação.

*Boa sorte. O código está em boas mãos.*
