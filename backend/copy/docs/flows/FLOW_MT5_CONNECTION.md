# Fluxo de Conexão Rígido (Strict MT5 Connection)

> **Maturidade:** Draft (Aguardando Implementação)
> **Componentes:** Master Sender, Client Copier
> **Prioridade:** Crítica (Segurança)

Este documento define o padrão obrigatório para o estabelecimento de conexões entre os serviços Python (`aibot-backend`) e o terminal MetaTrader 5.

## 1. Princípios de Segurança (Regras de Ouro)

1.  **Autoridade Única (Single Source of Truth):**
    A conexão **só pode ocorrer** se os parâmetros `mt5_id` (Login) e `mt5_path` (Executável) forem fornecidos pelo Banco de Dados/API. Configurações locais (`config_*.json`) são ignoradas para este fim ou usadas apenas como fallback em ambiente de desenvolvimento explícito.

2.  **Abortar por Padrão (Fail Fast):**
    Se os dados de conexão estiverem incompletos, nulos ou vazios no banco de dados, o serviço Python deve ser encerrado imediatamente (`sys.exit(1)`). Não deve haver tentativa de "adivinhar" o terminal.

3.  **Path Específico (Strict Path):**
    O Python deve invocar o método de inicialização apontando explicitamente para o executável: `mt5.initialize(path=DB_PATH)`. O "Observer Mode" (esperar qualquer terminal abrir) fica proibido em produção.

4.  **Validação de Identidade (Identity Match):**
    Após a inicialização, o ID da conta conectada (`mt5.account_info().login`) DEVE ser comparado com o `mt5_id` esperado.
    *   **Sucesso:** IDs coincidem.
    *   **Falha:** IDs divergem -> **Kill Switch** (Chamar `mt5.shutdown()` e encerrar processo).

## 2. Diagrama de Fluxo

```mermaid
graph TD
    Start([Início do Serviço Python]) --> FetchDB[Buscar Config na API /users/me]
    
    FetchDB --> HasConfig{Recebeu MT5_ID e PATH?}
    HasConfig -- Não --> Fatal1[PADRÃO DE SEGURANÇA: ABORTAR\n(Config Incompleta)]
    
    HasConfig -- Sim --> Init[mt5.initialize(path=PATH)]
    
    Init --> CheckInit{Inicializou?}
    CheckInit -- Não --> LogError[Log Erro + Retry Limitado]
    LogError --> Fatal2[ABORTAR após N tentativas]
    
    CheckInit -- Sim --> GetAccount[mt5.account_info()]
    
    GetAccount --> Validate{Login Atual == MT5_ID BD?}
    Validate -- Não --> KillSwitch[KILL SWITCH ATIVADO\nConta Errada/Demo Detectada]
    KillSwitch --> Shutdown[mt5.shutdown()]
    Shutdown --> Fatal3[Encerrar Processo]
    
    Validate -- Sim --> Success([✅ CONEXÃO SEGURA ESTABELECIDA])
    Success --> WorkLoop[Iniciar Loop de Trabalho]
```

## 3. Detalhamento Técnico

### Passos de Validação

1.  **Bootstrapping:**
    Ao iniciar, o serviço (`Master` ou `Client`) autentica na API e requisita seus dados de perfil.
    ```python
    user_data = api.get_profile()
    required_login = user_data['allowed_mt5_id']
    required_path = user_data['mt5_path']
    ```

2.  **Verificação de Pré-requisitos:**
    ```python
    if not required_login or not required_path:
        logger.critical("SEGURANÇA: Credenciais MT5 não encontradas no servidor. Abortando.")
        sys.exit(1)
    ```

3.  **Conexão Direcionada:**
    ```python
    if not mt5.initialize(path=required_path):
        logger.critical(f"Falha ao iniciar MT5 no path: {required_path}")
        return False
    ```

4.  **Validação de Identidade (O Guardião):**
    ```python
    current_info = mt5.account_info()
    if current_info.login != int(required_login):
        logger.critical(f"FATAL: Conta incorreta detectada! Esperado: {required_login}, Encontrado: {current_info.login}")
        mt5.shutdown()
        sys.exit(1) # Kill Switch
    ```

## 4. Auditoria e Logs

Todas as falhas de conexão devem gerar logs de nível `CRITICAL` localmente e, se possível, enviar um alerta para a API informando que o cliente falhou na verificação de segurança.
