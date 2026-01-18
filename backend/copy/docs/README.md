# 📚 Zulfinance CopyTrading - Documentação Oficial

Bem-vindo à base de conhecimento do projeto. Esta documentação foi estruturada para guiar desde novos desenvolvedores até mantenedores experientes através da arquitetura, operação e manutenção do sistema.

---

## 🧭 Mapa de Navegação

## 📚 Documentação

### Arquitetura e Visão Geral
- [Visão Geral do Sistema](architecture/SYSTEM_OVERVIEW_V1.md) - Arquitetura completa com diagramas
- [Componentes GUI](components/GUI_OVERVIEW.md) - Frontend Tauri e integração com Python
- [Arquitetura MT5](architecture/MT5_ARCHITECTURE.md) - Conexão, fluxos de dados e detecção de sinais

### Desenvolvimento Python
- [Guia de Desenvolvimento Python](development/PYTHON_DEV_GUIDE.md) - Guia completo para desenvolvedores Python
- [Erros Críticos](troubleshooting/CRITICAL_ERRORS.md) - Erros fatais documentados e soluções
- [Guia de Build](development/BUILD_GUIDE.md) - Processo completo de build e deploy
- [Requirements](setup/REQUIREMENTS.md) - Dependências e versões críticas

### API e Banco de Dados
- [Endpoints da API](api/ENDPOINTS.md) - Documentação completa da API Rust
- [Schema do Banco](database/SCHEMA_V1.md) - Estrutura das tabelas e relacionamentos

### Setup e Configuração
- [Configuração de Ambiente](setup/ENVIRONMENT.md) - Setup completo (Rust, Node, Python, Tauri)
- [Problemas Comuns](troubleshooting/COMMON_ISSUES.md) - Troubleshooting e soluções

### Testes e QA
- [Checklist de QA](testing/QA_CHECKLIST.md) - Roteiro de testes manuais

### Equipe e Processos
- [Mandatos Git](team/GIT_MANDATES.md) - Regras de Git e estratégia de branches
- [Rituais e Cultura](team/RITUALS_AND_CULTURE.md) - Valores e processos da equipe
- [Prompts de Onboarding](team/) - Guias específicos por role (Architect, Backend, Frontend, Core Python, QA)
- **[Segurança V2](security/V2_ARCHITECTURE_SECURITY.md)**: Documentação sobre a arquitetura de tabelas Active/History e Prevenção de Zombie Orders.

### 🛡️ Segurança & Auditoria
Princípios e práticas para manter o sistema protegido:

- **[Arquitetura de Segurança](SECURITY_ARCHITECTURE.md)**: Visão geral da fundação de segurança do sistema.
- **[Políticas de Banco de Dados](security/DATABASE_SECURITY.md)**: Regras de acesso oficial, PRAGMAs SQL e **Logs de Auditoria**.
- **[Segurança Frontend-Backend](security/FRONTEND_INTEGRATION_SECURITY.md)**: Hardening de headers, CSP, interceptação de 401 e gestão de sessões.

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
