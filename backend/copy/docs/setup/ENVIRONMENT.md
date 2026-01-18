# 🛠️ Configuração de Ambiente (Environment Setup)

Guia para preparar a máquina de desenvolvimento no Windows.

## 1. Pré-requisitos Básicos
- **Sistema Operacional:** Windows 10/11 (Obrigatório para MetaTrader 5).
- **MetaTrader 5:** Instalado e logado nas contas de teste.

## 2. Linguagens & Ferramentas
### Rust (Backend API & Tauri)
- Instalar via `rustup-init.exe`.
- Comando de verificação: `cargo --version`.

### Node.js (Frontend GUI)
- Versão LTS recomendada (v18+).
- Instalar `pnpm` ou `npm` (usamos `npm` nos scripts).
- Comando: `node -v`, `npm -v`.

### Python (AI/Trading Logic)
- Versão: 3.10 ou superior (3.12 testada).
- **Importante:** Adicionar ao PATH do Windows.
- Dependências Globais:
  ```bash
  pip install pyinstaller MetaTrader5 requests
  ```

## 3. Configuração do Projeto

### Instalação de Dependências
```bash
# Raiz
# Nenhuma dependência específica na raiz, apenas scripts.

# Master Sender GUI
cd master_sender/gui
npm install

# Client Copier GUI
cd client_copier/gui
npm install
```

### Configuração do Banco de Dados
O banco `api_server/aibot.db` é criado automaticamente se não existir, mas para garantir a estrutura correta:
```bash
python scripts/utils/check_db_now.py
```

## 4. Build Manual (Procedimento de Hotfix)
Se alterar código Python, o Tauri pode não atualizar o binário. Use:
```powershell
# Para Master
./scripts/build/rebuild_master_clean.ps1

# Para Client
./scripts/build/rebuild_client_clean.ps1
```
Isso força o PyInstaller a gerar um novo `.exe` e o injeta na pasta do Tauri.
