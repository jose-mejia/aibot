# 📚 Zulfinance CopyTrading - Documentação Oficial

Bem-vindo à base de conhecimento do projeto. Esta documentação foi estruturada para guiar desde novos desenvolvedores até mantenedores experientes através da arquitetura, operação e manutenção do sistema.

---

## 🧭 Mapa de Navegação

### 🚀 Para Começar (Onboarding)
Se você acabou de chegar, comece por aqui:

- **[Visão Geral da Arquitetura](architecture/SYSTEM_OVERVIEW_V1.md)**: Entenda quem fala com quem (Master, API, Client).
- **[Configuração de Ambiente](setup/ENVIRONMENT.md)**: Prepare sua máquina (Rust, Python, Node, MT5).
- **[Interface & Sidecars](components/GUI_OVERVIEW.md)**: Entenda como o Frontend interage com o Python "escondido".

### 🧠 Core do Sistema (Deep Dive)
Documentação técnica profunda dos componentes:

- **[Esquema do Banco de Dados](database/SCHEMA_V1.md)**: Estrutura das tabelas `users` e `signals`.
- **[API Endpoints](api/ENDPOINTS.md)**: contrato da API Rust (Rotas, Payloads, Auth).
- **[Fluxos de Ordens](flows/FLOW_OPEN_ORDER.md)**: Diagramas detalhados de como uma ordem viaja do Master ao Client.
  - [Fluxo de Abertura](flows/FLOW_OPEN_ORDER.md)
  - [Fluxo de Modificação](flows/FLOW_MODIFY.md)
  - [Fluxo de Fechamento](flows/FLOW_CLOSE.md)
- **[Detecção de Ordens](ORDER_DETECTION.md)**: Como o Master "enxerga" as ordens no MT5.

### 🛠️ Manutenção & Operação
Guias para o dia-a-dia do desenvolvimento:

- **[Estado Atual & Contexto](devia/CURRENT_STATE.md)**: **(CRÍTICO)** Leia isso para saber o status atual do projeto (Hotfixes, versões).
- **[Guia de Troubleshooting](troubleshooting/COMMON_ISSUES.md)**: Soluções para erros conhecidos (Conexão MT5, Preço Inválido, etc).
- **[Checklist de QA](testing/QA_CHECKLIST.md)**: Roteiro para validar uma nova versão antes de liberar.

### 📜 Histórico e Memória
Registros de decisões e sessões passadas:

- **[Logs de Sessão](devia/CHAT_TRANSCRIPT_2026_01_04.md)**: Transcripts de sessões de debug importantes.
- **[Diários de Dev](devia/DEV_DIARY_LAST_3_DAYS.md)**: Resumos executivos do progresso recente.

---

## 🏷️ Glossário Rápido

- **Sidecar:** O processo Python executável que roda em background, controlado pelo Tauri.
- **Master:** A conta "fonte" dos sinais. Só monitora, nunca executa.
- **Client/Follower:** A conta "destino". Só executa, nunca gera sinais.
- **Ticket:** ID único de uma ordem no MT5. O Client mantém um mapa `MasterTicket -> ClientTicket`.
- **Broadcast:** O ato da API enviar um sinal recebido para todos os Clients conectados via WebSocket.
