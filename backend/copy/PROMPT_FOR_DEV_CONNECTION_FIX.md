# 🆘 PROMPT PARA DEV CORE (HOTFIX CONEXÃO MT5)

**Contexto:**
Estamos enfrentando um problema crítico onde o script Python ignora o `mt5_path` fornecido e conecta a qualquer instância MT5 aberta. Já tentamos recompilar o binário, mas o erro persiste. A suspeita agora recai sobre a própria chamada da biblioteca `MetaTrader5` ou permissões do Windows.

**Tarefa Técnica:**
Precisamos isolar o problema. Não tente consertar a aplicação completa (`SenderService`). Quero um script de diagnóstico isolado.

**Crie um arquivo chamado `debug_raw_connection.py` com o seguinte objetivo:**
1.  Define hardcoded o caminho do MT5 Master: `C:\Program Files\IC Markets Global01\terminal64.exe` (ajuste para o path real do usuário).
2.  Define hardcoded o ID esperado: `7409735`.
3.  Tenta realizar `mt5.initialize(path=MT5_PATH)`.
4.  **CRÍTICO:** Se falhar, deve imprimir `mt5.last_error()` completo.
5.  Se conectar, deve imprimir `mt5.account_info().login` para vermos se bateu.

**O que esperamos descobrir:**
- Se o erro for `(-10004, 'Path not found')`, é erro de string/escape no Windows.
- Se o erro for genérico, pode ser falta de permissão ou o MT5 demorando para responder.
- Se funcionar nesse script isolado, o bug está na nossa Classe `MT5Connector`.

**Execute este teste localmente e me traga o output exato.**
