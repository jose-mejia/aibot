# Erros Críticos e Como Evitá-los

## 🚨 Erros Fatais Documentados

Este documento lista todos os erros críticos encontrados durante o desenvolvimento, suas causas raízes e soluções definitivas.

---

## 1. Numpy 2.x Incompatibilidade

### Erro
```
ModuleNotFoundError: No module named 'numpy'
ImportError: numpy._core.multiarray failed to import
[PYI-xxxxx:ERROR] Failed to execute script 'main_sender' due to unhandled exception!
```

### Causa Raiz
- Numpy 2.0+ reestruturou módulos internos (`numpy.core` → `numpy._core`)
- MetaTrader5 5.0.5430 depende da estrutura antiga
- PyInstaller não consegue resolver dependências transitivas do numpy 2.x

### Solução Permanente
```bash
# 1. Desinstalar numpy atual
pip uninstall numpy -y

# 2. Instalar versão compatível
pip install "numpy<2"

# 3. Fixar versão em requirements.txt
echo "numpy>=1.26.0,<2.0" >> requirements.txt

# 4. Atualizar .spec
# hiddenimports=['MetaTrader5', 'requests', 'sender_service', 'numpy']
```

### Prevenção
- **NUNCA** rode `pip install --upgrade numpy` sem verificar compatibilidade
- Sempre fixe versões em `requirements.txt`
- Teste executável após qualquer atualização de dependências

---

## 2. Race Condition - Conexão MT5 Errada

### Erro
```
FATAL: Wrong Account! Expected 7409735, Found 11629107. Please switch accounts in MT5.
```

### Causa Raiz
O código original tinha um loop "Observer Mode" que esperava **qualquer** `terminal64.exe`:

```python
# ❌ CÓDIGO PROBLEMÁTICO
while True:
    if "terminal64.exe" in tasklist_output:
        break  # Encontrou QUALQUER terminal, prossegue
```

Quando Master e Client estavam abertos, o script conectava no primeiro que respondia.

### Solução Implementada
```python
# ✅ CÓDIGO CORRIGIDO
if not path:
    # Só usa Observer Mode se NÃO tiver path específico
    while True:
        if "terminal64.exe" in tasklist_output:
            break
else:
    logger.info(f"Skipping Observer Mode. Using path: {path}")
    # Vai direto para mt5.initialize(path=path)
```

### Prevenção
- Sempre configure `mt5_path` no banco de dados
- Nunca confie em auto-detecção em ambientes com múltiplos terminais
- Valide `account_info().login` após `initialize()`

---

## 3. PyInstaller Hidden Imports

### Erro
```
ImportError: No module named 'MetaTrader5'
ImportError: No module named 'requests'
```

### Causa Raiz
PyInstaller analisa imports estáticos. Imports dinâmicos ou dependências transitivas não são detectados.

### Solução
Sempre declare no arquivo `.spec`:

```python
a = Analysis(
    ['main_sender.py'],
    hiddenimports=[
        'MetaTrader5',
        'requests', 
        'sender_service',
        'numpy',
        'numpy.core',  # Necessário para MT5
    ],
    # ...
)
```

### Prevenção
- Teste executável após adicionar novas bibliotecas
- Use `--debug=imports` no PyInstaller para diagnosticar

---

## 4. Config Path em Executáveis

### Erro
```
Config file not found at: config_sender.json
```

### Causa Raiz
Quando empacotado, `__file__` aponta para um diretório temporário do PyInstaller.

### Solução
```python
if getattr(sys, 'frozen', False):
    # Rodando como executável
    base_dir = os.path.dirname(sys.executable)
else:
    # Rodando como script Python
    base_dir = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(base_dir, 'config_sender.json')
```

### Prevenção
- Sempre use `sys.frozen` para detectar modo executável
- Teste caminhos de arquivo em ambos os modos

---

## 5. Processos Duplicados

### Erro
```
Multiple status updates from same account
Duplicate signal broadcasts
```

### Causa Raiz
Usuário inicia Master/Client múltiplas vezes sem fechar instâncias anteriores.

### Solução
```python
LOCK_FILE = os.path.join(os.environ.get('TEMP', ''), 'aibot_master.lock')

def check_single_instance():
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, 'r') as f:
            old_pid = int(f.read().strip())
            try:
                os.kill(old_pid, 9)  # Mata processo antigo
            except OSError:
                pass
    
    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))
```

### Prevenção
- Sempre implemente single instance lock
- Use `taskkill` em scripts de build para limpar processos

---

## 6. API 404 - Status Endpoint

### Erro
```
GET http://localhost:8000/mt5/status/2 404 (Not Found)
Failed to load MT5 status: Error: MT5 status not available
```

### Causa Raiz
O endpoint `/mt5/status/{user_id}` retorna 404 se:
1. Python sidecar não está rodando
2. Python sidecar não enviou status ainda (primeiro POST leva ~60s)
3. Servidor Rust não está rodando

### Solução
**Backend (Rust):**
```rust
// Retornar 200 com status vazio em vez de 404
if status.is_none() {
    return Ok(Json(json!({
        "status": "pending",
        "message": "Waiting for first update from Python service"
    })));
}
```

**Frontend:**
```typescript
// Retry com backoff exponencial
const loadStatus = async () => {
    try {
        const data = await api.getMT5Status(userId);
        if (data.status === 'pending') {
            setTimeout(loadStatus, 5000);  // Retry em 5s
        }
    } catch (err) {
        // Não mostrar erro nos primeiros 30s
    }
};
```

### Prevenção
- Implementar grace period no frontend
- Logar claramente quando Python sidecar inicia

---

## 7. HMAC Signature Mismatch

### Erro
```
SECURITY ALERT: Token Rejected. Response: Invalid signature
```

### Causa Raiz
Timestamp ou payload JSON não estão sincronizados entre cliente e servidor.

### Solução
```python
# Cliente (Python)
timestamp = str(int(time.time() * 1000))
payload_str = json.dumps(payload, sort_keys=True, separators=(',', ':'))
canonical = f"{timestamp}.{payload_str}"
signature = hmac.new(token.encode(), canonical.encode(), hashlib.sha256).hexdigest()

headers = {
    "X-Timestamp": timestamp,
    "X-Signature": signature
}
```

```rust
// Servidor (Rust)
let canonical = format!("{}.{}", timestamp, payload_json);
let expected_sig = hmac_sha256(&token, &canonical);
if signature != expected_sig {
    return Err(StatusCode::UNAUTHORIZED);
}
```

### Prevenção
- Use `sort_keys=True` e `separators=(',', ':')` para JSON determinístico
- Valide timestamp (rejeitar se > 5 minutos de diferença)

---

## 8. MT5 Initialize Timeout

### Erro
```
Initialize failed with path: (1, 'Terminal: not found')
Failed to connect to MT5 Terminal after 3 attempts.
```

### Causa Raiz
- MT5 não está aberto
- Path do executável está incorreto
- MT5 está travado/carregando

### Solução
```python
# Retry com backoff
for attempt in range(30):  # 30 tentativas = ~30s
    if mt5.initialize(path=path):
        break
    logger.warning(f"Attempt {attempt+1}/30 failed. Retrying...")
    time.sleep(1)
```

### Prevenção
- Validar `mt5_path` antes de salvar no banco
- Instruir usuário a abrir MT5 manualmente antes de iniciar app

---

## Checklist de Validação Pré-Deploy

Antes de fazer build de produção, verifique:

- [ ] `pip list | grep numpy` mostra versão `<2.0`
- [ ] Arquivo `.spec` inclui todos os `hiddenimports`
- [ ] `mt5_path` está correto no banco de dados
- [ ] Servidor Rust está rodando (`cargo run`)
- [ ] MT5 está aberto na conta correta
- [ ] Nenhum processo duplicado rodando
- [ ] Logs mostram "Skipping Observer Mode" (se path fornecido)
- [ ] Executável testado manualmente antes do Tauri build

---

## Comandos de Diagnóstico Rápido

```bash
# Verificar versão do Numpy
pip show numpy

# Listar processos Python/MT5
tasklist | findstr "python terminal64"

# Testar executável diretamente
./master_sender/gui/src-tauri/target/release/sender-service.exe --token=test

# Ver logs em tempo real
tail -f sender.log

# Limpar lock files
del %TEMP%\aibot_*.lock

# Rebuild completo
powershell -ExecutionPolicy Bypass -File rebuild_master_clean.ps1
```
