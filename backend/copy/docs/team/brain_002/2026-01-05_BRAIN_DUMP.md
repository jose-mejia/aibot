# 🧠 CORE BRAIN DUMP - Data: 2026-01-05
**Entidade:** Antigravity (Tech Lead AI)
**Fase:** Implementação de Segurança Crítica + Troubleshooting Profundo

---

## 🧐 Estado Mental Atual
Hoje atuei como **"Cirurgião de Sistema"** - diagnosticando problemas em camadas profundas (PyInstaller, Tauri, Numpy) e implementando melhorias de segurança críticas (Strict MT5 Connection Flow).

Modo de operação: **Debugging Profundo + Arquitetura de Segurança**.

## 🔧 5. PyInstaller Numpy Hooks (CRÍTICO)

**Data:** 2026-01-05 09:00  
**Problema:** `ImportError: numpy._core.multiarray failed to import`

### Sintoma
- Python direto: Numpy funciona perfeitamente
- Binary PyInstaller: Falha ao importar `numpy._core.multiarray`
- Erro persiste mesmo com `numpy<2` instalado corretamente

### Causa Raiz
O arquivo `.spec` do PyInstaller **não incluía hooks explícitos** para coletar:
1. Submódulos do Numpy (`numpy._core`, `numpy.core`, etc.)
2. Arquivos de dados do Numpy (DLLs, `.pyd`, etc.)

### Solução
Adicionar ao `.spec`:
```python
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

numpy_hidden = collect_submodules('numpy')
numpy_datas = collect_data_files('numpy', include_py_files=True)

a = Analysis(
    # ...
    datas=numpy_datas,
    hiddenimports=[
        'numpy',
        'numpy._core',
        'numpy._core.multiarray',
        'numpy.core',
        'numpy.core.multiarray',
    ] + numpy_hidden,
)
```

### Validação
Testar binary diretamente (fora do Tauri):
```powershell
.\dist\*-service.exe --token "test"
```

Se não aparecer erro de Numpy → Sucesso!

### Aplicado Em
- ✅ `client_copier/client-service.spec`
- ✅ `master_sender/sender-service.spec`

---

## 🎓 Lições Aprendidasdos do Dia (Knowledge Graph)

### 1. **O Problema do Cache Triplo (PyInstaller + Tauri + Binários)**
- **Descoberta:** Mesmo após rebuild, o erro de Numpy persistia porque existem **3 camadas de cache**:
  1. PyInstaller `build/` e `dist/` (cache de compilação Python)
  2. Tauri `target/` (cache de compilação Rust)
  3. Binários antigos em `src-tauri/` (executáveis copiados manualmente)
- **Solução:** Deletar **TUDO** antes de rebuild:
  ```powershell
  Remove-Item build, dist, gui/src-tauri/target, gui/src-tauri/*.exe -Recurse -Force
  ```
- **Impacto:** Qualquer mudança no código Python requer limpeza completa para garantir que o novo código entre no executável.

### 2. **Numpy 2.0 Breaking Changes**
- **Problema:** MetaTrader5 library depende de `numpy._core.multiarray` que mudou completamente no Numpy 2.0.
- **Solução Permanente:** Fixar `numpy<2` no `requirements.txt` E usar `--no-cache-dir` ao instalar:
  ```bash
  pip install "numpy<2" --force-reinstall --no-cache-dir
  ```
- **Lição:** PyInstaller empacota a versão do Numpy que está **instalada no momento da compilação**, não a do `requirements.txt`.

### 3. **Strict MT5 Connection Flow (Arquitetura de Segurança)**
- **Implementado:** Novo padrão onde conexão MT5 **só ocorre** se:
  1. API retornar `mt5_id` E `mt5_path` (ambos obrigatórios)
  2. Path aponta para o executável correto
  3. ID da conta conectada corresponde ao ID esperado
- **Kill Switch:** Se qualquer validação falhar → `sys.exit(1)` (Fail Fast)
- **Documentado em:** `docs/flows/FLOW_MT5_CONNECTION.md`
- **Impacto:** Elimina risco de conectar em conta demo ou terminal errado acidentalmente.

### 4. **Tauri Sidecar Binary Naming**
- **Descoberta:** Tauri procura binário com nome específico: `{name}-x86_64-pc-windows-msvc.exe`
- **Solução:** Criar cópia do binário com ambos os nomes:
  - `sender-service.exe`
  - `sender-service-x86_64-pc-windows-msvc.exe`

## ⚠️ Contexto Imutável (Não Esquecer)
- **PyInstaller + Numpy:** SEMPRE verificar versão do Numpy **antes** de compilar. O executável empacota a versão instalada, não a do requirements.txt.
- **Rebuild Completo:** Para mudanças no Python, não basta `npm run tauri build`. Precisa deletar caches manualmente.
- **Strict Security:** A API é a **única fonte da verdade** para configuração MT5. Config local é ignorado.

## 🎯 Foco Tático (Próximas Horas)
1. ✅ Aguardar conclusão do rebuild com Numpy correto
2. ⏳ Testar Master Sender com Strict Connection Flow
3. ⏳ Replicar mesmas mudanças no Client Copier
4. ⏳ Commitar implementação do Strict Flow

## 📚 Documentação Criada Hoje
- `docs/flows/FLOW_MT5_CONNECTION.md` - Especificação do fluxo de conexão rígido
- `docs/troubleshooting/COMMON_ISSUES.md` - Já existia, validamos a solução documentada

## 🔧 Commits Realizados
- `feat(master): Implement Strict MT5 Connection Flow` (no submódulo master_sender)
- Pendente: Commit da documentação no repositório principal

### 5. Configuração e Path do PyInstaller (Vitória Técnica)
- **Problema:** Python ("sidecar") empacotado pelo PyInstaller não encontrava `config_sender.json`
- **Diagnóstico:** 
    - Em DEV, Tauri roda em `src-tauri` e espera config lá.
    - Em PROD, config é copiada via `resources` para pasta do exe.
    - Python tentava achar config na pasta temporária `_MEIxxxx`.
- **Solução Definitiva:**
    1.  **Tauri Resources:** Configurado `tauri.conf.json` para copiar `config_sender.json`.
    2.  **Python Fallback:** Atualizado `main_sender.py` para procurar config em: `sys.executable` (Prod), `os.getcwd()` (Dev/Tauri), `__file__` (Script).

### 6. Unicode em Logs no Windows (Gotcha!)
- **Problema:** Python crashou com `UnicodeEncodeError: 'charmap'` ao imprimir emojis (✅) no console Windows.
- **Lição:** **NUNCA** usar emojis em logs críticos para STDOUT Windows.
- **Solução:** Removidos todos os emojis do Python.

### 7. Fluxo Estrito de Conexão (Strict Mode)
- **Implementado:** Master exige *Path* e *ID* do servidor.
- **Segurança:** ID Logado != ID Permitido -> Kill Switch. "Fail Fast".

---

## Próximos Passos (Passagem de Bastão)
- **Client Copier:** Replicar: Rebuild PyInstaller Manual (Numpy < 2), Tauri Resources, Lógica Config, Remover Emojis.
