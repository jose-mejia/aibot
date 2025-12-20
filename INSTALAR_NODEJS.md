# 📦 Como Instalar Node.js e npm no Windows

## 🎯 O que é necessário?

Para rodar o frontend, você precisa de:
- **Node.js** (versão 16 ou superior)
- **npm** (vem junto com Node.js)

---

## 🚀 Método 1: Instalação Direta (Recomendado)

### Passo 1: Baixar Node.js

1. Acesse: https://nodejs.org/
2. Você verá duas opções:
   - **LTS** (Long Term Support) - Recomendado ✅
   - **Current** (Versão mais recente)

3. **Clique em "LTS"** para baixar a versão estável

### Passo 2: Instalar Node.js

1. Execute o arquivo baixado (ex: `node-v20.x.x-x64.msi`)
2. Clique em **"Next"** na tela de boas-vindas
3. Aceite os termos de licença e clique **"Next"**
4. **IMPORTANTE:** Deixe marcado:
   - ✅ **Automatically install the necessary tools**
   - ✅ **Add to PATH** (já vem marcado por padrão)
5. Clique em **"Next"** e depois **"Install"**
6. Aguarde a instalação
7. Clique em **"Finish"**

### Passo 3: Verificar Instalação

Abra um **NOVO** PowerShell ou CMD e digite:

```bash
node --version
```

**Deve mostrar:** `v20.x.x` ou similar

```bash
npm --version
```

**Deve mostrar:** `10.x.x` ou similar

**✅ Se aparecer as versões, está instalado corretamente!**

---

## 🔧 Método 2: Usando Chocolatey (Opcional)

Se você já tem Chocolatey instalado:

```powershell
choco install nodejs-lts
```

---

## 🐛 Solução de Problemas

### Problema: "node não é reconhecido como comando"

**Solução:**

1. **Reinstalar Node.js** marcando "Add to PATH"
2. **OU adicionar manualmente ao PATH:**
   - Pressione `Win + R`
   - Digite: `sysdm.cpl` e pressione Enter
   - Aba "Avançado" → "Variáveis de Ambiente"
   - Em "Variáveis do sistema", encontre "Path"
   - Clique em "Editar"
   - Adicione: `C:\Program Files\nodejs\`
   - Clique "OK" em tudo
   - **Reinicie o terminal**

### Problema: Versão muito antiga

**Solução:**

1. Desinstale Node.js antigo:
   - Painel de Controle → Programas → Desinstalar
   - Procure por "Node.js" e desinstale

2. Instale a versão LTS mais recente do site oficial

### Problema: npm não funciona

**Solução:**

```bash
# Atualizar npm
npm install -g npm@latest

# Verificar versão
npm --version
```

---

## ✅ Verificação Completa

Após instalar, teste tudo:

```bash
# Verificar Node.js
node --version
# Deve mostrar: v16.x.x ou superior

# Verificar npm
npm --version
# Deve mostrar: 8.x.x ou superior

# Testar instalação de pacote
npm install -g yarn
# Se não der erro, está funcionando!
```

---

## 📝 Próximos Passos

Após instalar Node.js e npm:

1. **Abrir terminal** na pasta do frontend:
   ```bash
   cd C:\Users\josemejia\dev\python\aibot\frontend
   ```

2. **Instalar dependências:**
   ```bash
   npm install
   ```

3. **Rodar o frontend:**
   ```bash
   npm start
   ```

---

## 🎯 Resumo

1. ✅ Baixar Node.js LTS de: https://nodejs.org/
2. ✅ Instalar marcando "Add to PATH"
3. ✅ Verificar com `node --version` e `npm --version`
4. ✅ Pronto para usar!

---

## 📞 Precisa de Ajuda?

Se tiver problemas:
- Certifique-se de baixar da fonte oficial: https://nodejs.org/
- Use a versão LTS (não a Current)
- Marque "Add to PATH" durante instalação
- Reinicie o terminal após instalar

