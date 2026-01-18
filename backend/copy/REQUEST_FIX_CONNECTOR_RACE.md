# 🆘 REQUEST: CORREÇÃO DE RACE CONDITION NO MT5 CONNECTOR

**Prioridade:** ALTA (Bloqueia Conexão Master)
**Componente:** `master_sender/mt5_connector.py` (e `client_copier` se aplicável)
**Responsável:** Core Python Dev

## 🛑 O Problema
O modo "Observer" atual (linhas 23-43) espera que **qualquer** processo `terminal64.exe` apareça no `tasklist` antes de tentar conectar.
Em um cenário com 2 terminais (Master e Client), se o Client já estiver aberto, o loop quebra imediatamente. O `mt5.initialize(path=...)` é chamado, mas devido a limitações da lib `MetaTrader5` com múltiplas instâncias, ele acaba se "agarrando" à instância já ativa do Client, ignorando o `path` do Master.

## 🛠️ A Solução Técnica Solicitada
Precisamos alterar o método `connect` em `MT5Connector` para:

1.  **Pular o Loop de Observer se `path` for fornecido.**
    Se temos um caminho específico (`path`), não devemos esperar "qualquer terminal". Devemos tentar inicializar aquele caminho imediatamente. A lib MT5 deve se encarregar de abri-lo se não estiver rodando.

2.  **Lógica Sugerida:**
    ```python
    # Se NÃO tem path, use o Observer (comportamento antigo para fallback)
    if not path:
        # Loop do tasklist...
        pass
    else:
        logger.info(f"Target Path provided: {path}. Skipping Observer Mode.")
    
    # ... segue para mt5.initialize(path=path)
    ```

3.  **Retentativa Inteligente:**
    Se conectar na conta errada (Wrong Account), faça `mt5.shutdown()` e tente novamente na próxima iteração do loop de retry.

## ✅ Critérios de Aceite
- O script deve tentar abrir o MT5 do Master MESMO se o do Client já estiver aberto.
- O log deve mostrar `Skipping Observer Mode` quando o path for usado.
