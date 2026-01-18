# 🏗️ Visão Geral da Arquitetura (System Overview)

## 🔄 Diagrama de Componentes

```mermaid
graph TD
    User[Usuário] -->|Usa| GUI_Master[Master Sender GUI (Tauri)]
    User -->|Usa| GUI_Client[Client Copier GUI (Tauri)]
    
    subgraph "Master Side"
        GUI_Master -->|Inicia| Py_Master[Python Service (Sender)]
        Py_Master -->|Monitora| MT5_Master[MT5 Terminal (Master)]
    end
    
    subgraph "Client Side"
        GUI_Client -->|Inicia| Py_Client[Python Service (Copier)]
        Py_Client -->|Executa| MT5_Client[MT5 Terminal (Client)]
    end
    
    subgraph "Backend Core (Rust)"
        API[API Server (Rust / Axum)]
        DB[(SQLite: aibot.db)]
        API -->|Lê/Escreve| DB
    end
    
    %% Comunicação
    Py_Master -->|HTTP POST (Sinal)| API
    API -->|WebSocket (Broadcast)| Py_Client
    
    %% Configuração
    Py_Master -.->|HTTP GET (Config)| API
    Py_Client -.->|HTTP GET (Config)| API
```

## 🧩 Responsabilidades

### 1. API Server (Rust)
- **Cérebro Central:** Autentica usuários e gerencia permissões.
- **Single Source of Truth:** Único componente com acesso direto ao banco de dados SQLite.
- **Broadcast:** Recebe sinais do Master e distribui para os Clients via WebSocket.

### 2. Master Sender (Python)
- **Observador:** Monitora o terminal MT5 em busca de novas ordens ou modificações.
- **Passivo:** Não executa ordens, apenas lê.
- **Relator:** Envia qualquer alteração detectada para a API.

### 3. Client Copier (Python)
- **Executor:** Recebe sinais da API e replica no MT5 local.
- **Segurança:** Aplica regras de arredondamento e validação (SafetyGuard) antes de enviar a ordem.
- **Mapeamento:** Mantém um mapa local de `Ticket Master -> Ticket Client` para gerenciar modificações futuras.

## 🔐 Segurança
- **Token JWT:** Todo acesso à API exige autenticação.
- **HMAC:** Comunicação entre processos Python e interface Tauri é assinada.
- **Isolamento:** Interface gráfica não tem acesso direto ao Banco ou ao MT5; tudo passa pelos serviços backend.
