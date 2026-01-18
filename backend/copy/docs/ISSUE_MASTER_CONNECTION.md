# 🔴 PROBLEMA: Master não conecta no MT5 correto

**Data:** 2026-01-04  
**Status:** 🔧 EM CORREÇÃO

---

## 🎯 SINTOMA

O Master Sender tenta conectar no MT5 mas sempre pega o MT5 errado:

```
Expected: 7409735 (Master)
Found: 11629107 (Client)
```

---

## 🔍 CAUSA RAIZ

O código Python do Master **NÃO está carregando o `mt5_path` do servidor**.

**Evidência:**
- ✅ Banco de dados TEM o path: `C:\Program Files\IC Markets Global01\terminal64.exe`
- ✅ Código Python TEM a lógica para carregar o path
- ❌ Log NÃO mostra `"Loaded MT5 Path from server: ..."`
- ❌ Executável do Tauri está usando **código antigo**

---

## 🔧 SOLUÇÃO

### Opção 1: Rebuild do Executável (DEFINITIVO)

```bash
cd master_sender/gui
npm run tauri build
```

Isso vai:
1. Recompilar o frontend
2. Empacotar o Python atualizado
3. Gerar novo executável com o código correto

### Opção 2: Teste Rápido (TEMPORÁRIO)

1. Feche o MT5 do Client (11629107)
2. Deixe APENAS o MT5 do Master aberto (7409735)
3. Reinicie o Master Sender

Se funcionar, confirma que o problema é o path.

---

## ✅ VALIDAÇÃO

Após o rebuild, o log deve mostrar:

```
Loaded MT5 ID from server: 7409735
DEBUG: server_path received = 'C:\Program Files\IC Markets Global01\terminal64.exe' (type: <class 'str'>)
Loaded MT5 Path from server: C:\Program Files\IC Markets Global01\terminal64.exe
Connected to MT5 Terminal. Active Account: 7409735  ✅
```

---

## 📋 CHECKLIST

- [ ] Rebuild do Master Sender concluído
- [ ] Master conecta na conta correta (7409735)
- [ ] Log mostra "Loaded MT5 Path from server"
- [ ] Ordem manual no Master é detectada
- [ ] Sinal aparece no banco de dados
- [ ] Client recebe e copia a ordem

---

**Próximo Passo:** Aguardar conclusão do build e testar.
