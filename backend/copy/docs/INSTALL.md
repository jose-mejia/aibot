# Guia de Instalação e Execução - Trade Copier (Seguidora)

Este guia explica como configurar um novo PC ou VPS do zero para rodar o sistema de cópia.

## 1. Instalação do Python
Recomendamos a versão **Python 3.11** (compatível e estável com MetaTrader5).

1.  Acesse o site oficial: [https://www.python.org/downloads/release/python-3119/](https://www.python.org/downloads/release/python-3119/)
2.  Baixe o **Windows installer (64-bit)**.
3.  **MUITO IMPORTANTE**: Na primeira tela da instalação, marque a caixinha:
    - [x] **Add Python.exe to PATH** (Adicionar Python ao PATH)
4.  Clique em **Install Now**.
5.  Ao finalizar, clique em **Disable path length limit** (se aparecer).

## 2. Preparar os Arquivos
1.  Copie a pasta `copy` inteira do seu projeto original para o novo PC (pode ser na Área de Trabalho ou em `C:\Bot\copy`).
2.  Esta pasta deve conter:
    - `observer.py` (Monitor da Master)
    - `main.py` (Copiador)
    - `copier_service.py`
    - `safety.py`
    - `utils.py`
    - `requirements.txt`
    - `config.json`
    - `accounts.json`
    - `symbols.json`

## 3. Criar Ambiente Virtual (Recomendado)
Embora não seja obrigatório em um PC dedicado, é uma boa prática para evitar conflitos.

1.  Abra o Prompt de Comando (CMD) dentro da pasta `copy`.
2.  Rode o comando para criar o ambiente:
    ```cmd
    python -m venv venv
    ```
3.  Ative o ambiente:
    ```cmd
    venv\Scripts\activate
    ```
    *Você verá um `(venv)` aparecer no começo da linha do terminal.*

## 4. Instalar Dependências
1.  Com o ambiente ativado, instale as bibliotecas necessárias:
    ```cmd
    pip install -r requirements.txt
    ```

## 5. Configurar as Contas
1.  Certifique-se de que os Terminais MT5 (Master e Seguidores) estão instalados neste PC.
2.  **Abra o arquivo `accounts.json`**.
3.  Atualize o `path` (caminho) para apontar para o `terminal64.exe` correto neste novo PC. 
    - Exemplo: `C:\Program Files\MetaTrader 5 IC Markets\terminal64.exe`
4.  Preencha Login, Senha e Servidor corretamente.
5.  (Opcional) Ajuste `symbols.json` se operar ativos exóticos que precisam de mais tolerância de Spread/Slippage.

## 6. Rodar o Robô (Arquitetura Dupla)
Você precisará abrir **DUAS janelas** do Prompt de Comando (CMD).

### Janela 1: O Espião (Master)
Este script conecta na conta Master e monitora as ordens.
```cmd
venv\Scripts\activate
python observer.py
```
*Deve aparecer: "Connected. Monitoring positions..."*

### Janela 2: O Copiador (Seguidores)
Este script lê as ordens do Espião e replica nos seguidores.
```cmd
venv\Scripts\activate
python main.py
```
*Deve aparecer: "Copier Service Initialized..."*

---
**Dica**: Para deixar rodando 24/7 no VPS, não feche as janelas pretas. Apenas minimize-as. Se reiniciar o PC, lembre de abrir as duas novamente.
