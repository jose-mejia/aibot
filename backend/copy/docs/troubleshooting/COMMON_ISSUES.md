# 🔧 Troubleshooting e Erros Comuns

Este guia compila os erros mais frequentes encontrados durante o desenvolvimento e operação do Zulfinance CopyTrader e suas soluções.

---

## 1. Conexão MT5 e Build

### 🔴 Sintoma: "Wrong Account!" mesmo configurado corretamente
**Erro:** O log mostra `FATAL: Wrong Account! Expected X, Found Y`, mas no banco de dados o `mt5_path` está correto.
**Causa:** O **Tauri não atualizou o binário Python** durante o build. Ele está usando uma versão em cache antiga do `.exe` na pasta `src-tauri/binaries`.
**Solução:**
1. Execute o script de limpeza e rebuild manual:
   ```powershell
   ./scripts/build/rebuild_master_clean.ps1
   ```
   (Ou a versão correspondente para o Client).
2. Isso exclui a pasta `target`, compila o Python via PyInstaller e copia o novo `.exe` antes de rodar o build do Tauri.

### 🔴 Sintoma: "Python Sidecar Failed to Start"
**Erro:** A GUI abre, mas o Python morre imediatamente.
**Causa:**
1. Python não instalado ou fora do PATH.
2. Dependências (`MetaTrader5`) não instaladas no ambiente global.
3. Path do MT5 inválido ou terminal não instalado.
**Solução:**
- Verifique se consegue rodar `python` no terminal.
- Rode `pip list` e cheque se `MetaTrader5` está lá.
- Verifique o log do Tauri (`F12` > Console) para ver o erro exato do stdout.

---

## 2. Execução de Ordens (Trading)

### 🔴 Erro 10015: "Invalid Price"
**Erro:** O Client recebe o sinal mas falha ao abrir a ordem com erro 10015.
**Causa:** O preço enviado pelo Master tem mais casas decimais do que o permitido pelo símbolo no Client (ex: Bitcoin tem 2 casas, Master enviou 50000.12345).
**Solução:**
- O sistema já implementa arredondamento automático baseado em `symbol_info.digits`.
Lógica no `client_service.py`:
```python
price = round(signal['price'], symbol_info.digits)
```

### 🔴 Erro 10013: "Invalid Request"
**Causa:** Volume inválido (lote mínimo ou passo de lote incorreto).
**Solução:**
- O sistema ajusta o volume para ser múltiplo do `volume_step` e maior que `volume_min`. Verifique se o saldo da conta Client suporta o lote mínimo.

---

## 3. Comunicação API

### 🔴 WebSocket Desconectado / Não reconecta
**Sintoma:** Client para de receber sinais.
**Causa:** API Server caiu ou token expirou (validade de 24h).
**Solução:**
- Reinicie o Client Copier (ele renova o login automaticamente ao iniciar).
- Verifique se a API Rust está rodando na porta 8000.

### 🔴 Erro 401 Unauthorized
**Causa:** Token JWT expirado ou usuário inválido.
**Solução:** Logout e Login novamente na interface gráfica.
