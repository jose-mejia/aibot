# Build Process - Lições Aprendidas

## 🎯 Objetivo

Este documento garante que **nunca mais** teremos problemas de build relacionados a Numpy, cache ou binários desatualizados.

## 🔴 Problemas Resolvidos

### 1. Problema do "Triplo Cache"
**Sintoma:** Mesmo após rebuild, código antigo ainda executa.

**Causa:** Existem 3 camadas de cache:
1. PyInstaller (`build/`, `dist/`)
2. Tauri (`gui/src-tauri/target/`)
3. Binários copiados manualmente (`gui/src-tauri/*.exe`)

**Solução:** Deletar **TODOS** antes de rebuild.

### 2. Numpy 2.0 Breaking Changes
**Sintoma:** `ImportError: numpy._core.multiarray failed to import`

**Causa:** MetaTrader5 não é compatível com Numpy 2.x.

**Solução:** 
- Fixar `numpy<2` no ambiente
- Validar versão **ANTES** de cada build
- Usar `--no-cache-dir` ao instalar

### 3. Unicode em Logs (Windows)
**Sintoma:** `UnicodeEncodeError: 'charmap' codec can't encode character`

**Causa:** Emojis em logs Python + console Windows com encoding `cp1252`.

**Solução:** Remover **TODOS** os emojis dos logs Python.

### 4. Config Path Discovery
**Sintoma:** `Config file not found`

**Causa:** PyInstaller extrai para pasta temporária, config não é encontrado.

**Solução:**
- Adicionar config ao `tauri.conf.json` → `resources`
- Implementar busca em múltiplos paths no Python
- Copiar config para `src-tauri/` em dev mode

## ✅ Processo de Build Garantido

### Master Sender

```powershell
cd master_sender
.\rebuild_master_guaranteed.ps1
```

### Client Copier

```powershell
cd client_copier
.\rebuild_client_guaranteed.ps1
```

## 📋 Checklist de Build

Antes de cada build, confirme:

- [ ] Numpy versão < 2.0 (`pip show numpy`)
- [ ] Nenhum processo Python/MT5 rodando
- [ ] Caches deletados (`build/`, `dist/`, `target/`)
- [ ] Logs Python sem emojis
- [ ] Config presente em `src-tauri/` (dev mode)

## 🚨 Se o Build Falhar

### Erro: "ModuleNotFoundError: No module named 'numpy'"

1. Verificar versão: `pip show numpy`
2. Se for 2.x: `pip uninstall -y numpy && pip install "numpy<2" --no-cache-dir`
3. Rebuild completo: `.\rebuild_*_guaranteed.ps1`

### Erro: "Config file not found"

1. Verificar `tauri.conf.json` → `resources` contém config
2. Copiar manualmente: `Copy-Item config_*.json -Destination gui\src-tauri\`

### Erro: "ModuleNotFoundError: No module named 'numpy'" ou "ImportError: numpy._core.multiarray failed to import"

**Sintoma:** Binary PyInstaller falha ao importar Numpy, mesmo com `numpy<2` instalado.

**Causa:** O arquivo `.spec` não inclui hooks explícitos para coletar submódulos e DLLs do Numpy.

**Solução:** Atualizar o `.spec` com:
```python
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

numpy_hidden = collect_submodules('numpy')
numpy_datas = collect_data_files('numpy', include_py_files=True)

a = Analysis(
    # ...
    datas=numpy_datas,
    hiddenimports=[
        # ... outros imports
        'numpy',
        'numpy._core',
        'numpy._core.multiarray',
    ] + numpy_hidden,
)
```

Depois rebuild: `pyinstaller --clean --noconfirm *.spec`

## 📚 Referências

- [BRAIN_DUMP.md](./brain_002/2026-01-05_BRAIN_DUMP.md) - Lições detalhadas
- [DONT.md](./DONT.md) - Regra: "NÃO faça gambiarras de configuração"
- [FLOW_MT5_CONNECTION.md](../flows/FLOW_MT5_CONNECTION.md) - Strict Connection Flow

## 🎓 Princípios

1. **Fail Fast**: Se config/path inválido → Abortar imediatamente
2. **Single Source of Truth**: API é a única fonte de `mt5_id` e `mt5_path`
3. **No Gambiarras**: Soluções robustas, não temporárias
4. **Clean Slate**: Sempre deletar caches antes de rebuild crítico
