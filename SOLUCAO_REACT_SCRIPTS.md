# 🔧 Solução: Erro 'react-scripts' não é reconhecido

## ❌ Erro

```
'react-scripts' não é reconhecido como um comando interno
ou externo, um programa operável ou um arquivo em lotes.
```

## ✅ Solução

O problema é que as dependências do npm não foram instaladas. Você precisa instalar primeiro!

### Passo 1: Ir para pasta do frontend

```bash
cd C:\Users\josemejia\dev\python\aibot\frontend
```

### Passo 2: Instalar Dependências

```bash
npm install
```

**⏱️ Tempo:** 2-5 minutos (primeira vez pode demorar mais)

**✅ Você verá:**
```
added 1500+ packages, and audited 1501 packages in 2m
```

### Passo 3: Verificar Instalação

Verifique se a pasta `node_modules` foi criada:

```bash
dir node_modules
```

Deve mostrar uma lista de pastas.

### Passo 4: Rodar Frontend

Agora sim, pode rodar:

```bash
npm start
```

---

## 🔍 Por que acontece?

O `react-scripts` é uma dependência do projeto que precisa ser instalada via `npm install`. Sem isso, o npm não sabe onde encontrar o comando.

---

## 🐛 Outros Problemas Possíveis

### Problema: npm install dá erro

**Solução 1: Limpar cache**
```bash
npm cache clean --force
npm install
```

**Solução 2: Deletar node_modules e reinstalar**
```bash
# Deletar pasta node_modules (se existir)
rmdir /s node_modules  # Windows CMD
# ou
Remove-Item -Recurse -Force node_modules  # PowerShell

# Deletar package-lock.json (se existir)
del package-lock.json

# Reinstalar
npm install
```

### Problema: Erro de permissão

**Solução:**
```bash
# Executar como administrador ou:
npm install --legacy-peer-deps
```

### Problema: Versão do Node.js muito antiga

**Solução:**
- Verifique versão: `node --version`
- Precisa ser Node.js 16 ou superior
- Se for menor, atualize: https://nodejs.org/

---

## ✅ Checklist

- [ ] Está na pasta `frontend`?
- [ ] Rodou `npm install`?
- [ ] Pasta `node_modules` existe?
- [ ] Agora rodou `npm start`?

---

## 📝 Comandos Completos (Copiar e Colar)

```bash
# 1. Ir para pasta frontend
cd C:\Users\josemejia\dev\python\aibot\frontend

# 2. Instalar dependências (PRIMEIRO!)
npm install

# 3. Aguardar instalação terminar

# 4. Rodar frontend
npm start
```

---

## 🎯 Resumo

**O problema:** Dependências não instaladas  
**A solução:** Rodar `npm install` antes de `npm start`  
**Tempo:** 2-5 minutos para instalar

