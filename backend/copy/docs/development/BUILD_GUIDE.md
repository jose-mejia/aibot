# Build e Deploy - Guia Completo

## 📦 Processo de Build

Este documento detalha o processo completo de build dos componentes Python (Master Sender e Client Copier).

---

## Pré-requisitos

### Ambiente Python
```bash
python --version  # Deve ser 3.12.x
pip --version
```

### Dependências Instaladas
```bash
pip install -r requirements.txt
```

**Versões Críticas:**
- `numpy>=1.26.0,<2.0` ⚠️ **OBRIGATÓRIO**
- `MetaTrader5==5.0.5430`
- `pyinstaller==6.17.0`

### Ferramentas de Build
- Node.js 18+ (para Tauri)
- Rust 1.70+ (para Tauri)
- PowerShell 5.1+

---

## Build Manual (Recomendado)

### Master Sender

**Script:** `rebuild_master_clean.ps1`

```powershell
# Executar da raiz do projeto
powershell -ExecutionPolicy Bypass -File rebuild_master_clean.ps1
```

**O que o script faz:**

1. **Mata processos:**
   ```powershell
   taskkill /F /IM sender-service.exe /T 2>$null
   taskkill /F /IM master-sender.exe /T 2>$null
   ```

2. **Limpa cache:**
   ```powershell
   Remove-Item -Recurse -Force master_sender/gui/target
   Remove-Item -Recurse -Force master_sender/gui/dist
   Remove-Item -Recurse -Force master_sender/build
   Remove-Item -Recurse -Force master_sender/dist
   ```

3. **Recompila Python:**
   ```powershell
   cd master_sender
   pyinstaller sender-service.spec --clean --noconfirm
   ```

4. **Copia executável:**
   ```powershell
   Copy-Item dist/sender-service.exe gui/src-tauri/sender-service.exe
   ```

5. **Build Tauri:**
   ```powershell
   cd gui
   npm run tauri build
   ```

**Saída Esperada:**
```
✓ Frontend built successfully
✓ Python sidecar copied
✓ Tauri app bundled
📦 Executável: master_sender/gui/src-tauri/target/release/master-sender.exe
```

### Client Copier

**Script:** `rebuild_client_clean.ps1`

Processo idêntico ao Master, mas para o Client.

---

## Build Manual (Passo a Passo)

Se os scripts automáticos falharem, siga este processo:

### 1. Preparação

```bash
# Navegar para o diretório do componente
cd master_sender  # ou client_copier

# Verificar ambiente
pip list | grep -E "numpy|MetaTrader5|pyinstaller"

# Limpar builds anteriores
rm -rf build/ dist/ gui/target/ gui/dist/
```

### 2. Compilar Python com PyInstaller

```bash
pyinstaller sender-service.spec --clean --noconfirm
```

**Flags importantes:**
- `--clean`: Remove cache do PyInstaller
- `--noconfirm`: Sobrescreve sem perguntar
- `--debug=imports`: (opcional) Debug de imports

**Verificar saída:**
```bash
ls -lh dist/sender-service.exe
# Deve ter ~30-50 MB
```

### 3. Copiar para Tauri

```bash
cp dist/sender-service.exe gui/src-tauri/sender-service.exe
```

### 4. Build Frontend (Vite)

```bash
cd gui
npm install  # Primeira vez apenas
npm run build
```

**Saída esperada:**
```
vite v6.4.1 building for production...
✓ 1609 modules transformed.
dist/index.html                   0.46 kB
dist/assets/index-DOXpupEX.css   53.41 kB
dist/assets/index-BrXv7yez.js   322.73 kB
✓ built in 4.12s
```

### 5. Build Tauri

```bash
npm run tauri build
```

**Tempo esperado:** 3-5 minutos (primeira vez), 1-2 minutos (subsequentes)

**Saída:**
```
Compiling master-sender v0.1.0
Finished release [optimized] target(s) in 2m 34s
Bundling master-sender.exe
```

**Artefatos gerados:**
- `gui/src-tauri/target/release/master-sender.exe` (executável principal)
- `gui/src-tauri/target/release/bundle/nsis/ZulFinance_Master_0.1.0_x64-setup.exe` (instalador)

---

## Configuração do PyInstaller (.spec)

### Estrutura do Arquivo

```python
# sender-service.spec
a = Analysis(
    ['main_sender.py'],              # Entry point
    pathex=[],                        # Paths adicionais
    binaries=[],                      # DLLs externas
    datas=[],                         # Arquivos de dados
    hiddenimports=[                   # Imports não detectados
        'MetaTrader5',
        'requests',
        'sender_service',
        'numpy',                      # ⚠️ CRÍTICO
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],                      # Módulos a excluir
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='sender-service',
    debug=False,                      # True para debug
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                         # Compressão UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,                     # False para GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

### Customizações Importantes

**Incluir arquivos de dados:**
```python
datas=[
    ('config_sender.json', '.'),  # Copia config para raiz do exe
    ('assets/*', 'assets'),       # Copia pasta assets
],
```

**Excluir módulos pesados:**
```python
excludes=[
    'matplotlib',
    'pandas',
    'scipy',
],
```

**Debug mode:**
```python
exe = EXE(
    # ...
    debug=True,           # Ativa logs verbosos
    console=True,         # Mostra console
)
```

---

## Validação Pós-Build

### 1. Teste do Executável Python

```bash
cd master_sender/dist
./sender-service.exe --token=test_token_123
```

**Logs esperados:**
```
Starting Secure Master Sender...
Loaded MT5 Path from server: C:\...\terminal64.exe
Skipping Observer Mode...
Connected to MT5 Terminal. Active Account: 7409735
Sender Service Started. Monitoring Master Account...
```

**Erros comuns:**
- `ModuleNotFoundError: numpy` → Rebuild com numpy<2
- `Config file not found` → Verificar `config_sender.json` no mesmo diretório
- `FATAL: Wrong Account` → Verificar `mt5_path` no banco

### 2. Teste do Executável Tauri

```bash
cd master_sender/gui/src-tauri/target/release
./master-sender.exe
```

**Validações:**
- [ ] App abre sem erros
- [ ] Login funciona
- [ ] Python sidecar inicia (ver logs no console F12)
- [ ] Conexão MT5 estabelecida
- [ ] Dashboard mostra status

### 3. Verificar Tamanho dos Arquivos

```bash
# Python sidecar
ls -lh master_sender/dist/sender-service.exe
# Esperado: 30-50 MB

# Executável Tauri
ls -lh master_sender/gui/src-tauri/target/release/master-sender.exe
# Esperado: 15-25 MB

# Instalador NSIS
ls -lh master_sender/gui/src-tauri/target/release/bundle/nsis/*.exe
# Esperado: 40-60 MB
```

---

## Troubleshooting de Build

### Erro: "UPX is not available"

```bash
# Desabilitar UPX no .spec
upx=False,
```

### Erro: "Failed to execute script"

```bash
# Rebuild com debug
pyinstaller sender-service.spec --debug=all --clean

# Executar e capturar logs
./dist/sender-service.exe > build.log 2>&1
```

### Erro: "Tauri CLI not found"

```bash
cd gui
npm install @tauri-apps/cli --save-dev
```

### Build Muito Lento

```bash
# Usar cache do Cargo
export CARGO_INCREMENTAL=1

# Paralelizar build
cargo build --release -j 8
```

---

## Deploy em Produção

### 1. Preparar Artefatos

```bash
# Criar pasta de release
mkdir release/v1.0.0

# Copiar executáveis
cp master_sender/gui/src-tauri/target/release/master-sender.exe release/v1.0.0/
cp client_copier/gui/src-tauri/target/release/client-copier.exe release/v1.0.0/

# Copiar instaladores
cp master_sender/gui/src-tauri/target/release/bundle/nsis/*.exe release/v1.0.0/
cp client_copier/gui/src-tauri/target/release/bundle/nsis/*.exe release/v1.0.0/
```

### 2. Assinar Executáveis (Opcional)

```bash
# Windows Code Signing
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com master-sender.exe
```

### 3. Criar Checksums

```bash
cd release/v1.0.0
sha256sum *.exe > checksums.txt
```

### 4. Testar em Máquina Limpa

- [ ] Instalar em Windows sem Python
- [ ] Verificar se MT5 conecta
- [ ] Testar fluxo completo Master → Client

---

## CI/CD (Futuro)

### GitHub Actions Workflow

```yaml
name: Build Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Build Master
        run: powershell -File rebuild_master_clean.ps1
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: master-sender
          path: master_sender/gui/src-tauri/target/release/*.exe
```

---

## Checklist de Build

Antes de fazer build de produção:

- [ ] Numpy está em versão `<2.0`
- [ ] Todos os testes passam
- [ ] Código commitado no Git
- [ ] Versão atualizada em `tauri.conf.json`
- [ ] Changelog atualizado
- [ ] Build testado em modo dev
- [ ] Processos antigos mortos
- [ ] Cache limpo

Após build:

- [ ] Executável Python testado standalone
- [ ] Executável Tauri testado
- [ ] Logs verificados
- [ ] Conexão MT5 validada
- [ ] Tamanho dos arquivos razoável
- [ ] Checksums gerados
