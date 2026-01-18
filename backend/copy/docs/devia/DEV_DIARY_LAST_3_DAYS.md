# 📔 DIÁRIO DE DESENVOLVIMENTO (Últimos 3 Dias)
**Data de Registro:** 04/01/2026
**Contexto:** Correção Crítica de Conexão e Estabilização do Sistema

---

## 📅 DIAS 1-2: Auditoria, Organização e Segurança

### 1. Auditoria do Fluxo de Ordens
Realizamos uma auditoria completa no código para garantir que o sistema suporta "Todas as Ordens" (Manuais, Robôs, Scripts).
- **Descoberta:** O `master_sender` já estava configurado corretamente para ler `positions_get` sem filtros, capturando tudo.
- **Documentação:** Foram criados os diagramas de fluxo em `docs/flows/` (`FLOW_OPEN_ORDER.md`, etc).

### 2. Reestruturação do Projeto
Para preparar o projeto para escala, limpamos a raiz:
- **Docs:** Movido tudo para a pasta `docs/` com subpastas organizadas.
- **Scripts:** Criada pasta `scripts/` separando `utils` e `build`.
- **Limpeza:** Remoção de logs antigos e caches.

### 3. Segurança do Banco de Dados
Havia conflito entre bancos (`users.db` vs `aibot.db`).
- **Ação:** Unificamos tudo no **`api_server/aibot.db`**.
- **Segurança:** Implementamos travas no Python e no Rust para impedir que scripts acessem bancos errados.
- **Correção de Trade:** Corrigido o erro "Invalid Price" (10015) implementando arredondamento correto baseado nos dígitos do símbolo.

---

## 📅 DIA 3 (HOJE): O Problema da Conexão MT5

### 🛑 O Sintoma
Apesar de tudo configurado, o **Master Sender** insistia em conectar na conta MT5 errada (conectava na do Client `11629107` ao invés da Master `7409735`).

### 🕵️‍♂️ A Investigação
1.  **Checagem do Banco:** Verificamos via script Python direto no banco. O `mt5_path` estava salvo corretamente.
2.  **Checagem da API:** A API Rust estava retornando o dado corretamente.
3.  **Checagem do Log (A Pista):** Percebemos que o log do Master **não mostrava** a linha de debug que adicionamos hoje. Isso indicava que o código que estava rodando **não era o código que estávamos editando**.

### 🧩 O Diagnóstico
O framework **Tauri** (que cria a interface gráfica) estava empacotando uma versão antiga ("cacheada") do executável Python (`sender-service.exe`). Mesmo dando `npm run tauri build`, ele reutilizava o binário antigo, ignorando nossas correções no script `.py`.

### 🛠️ A Solução (O "Fix" Definitivo)
Tivemos que intervir manualmente no processo de build:
1.  **Compilação Manual:** Usamos `pyinstaller` diretamente na linha de comando para gerar um novo `sender-service.exe` limpo e atualizado.
2.  **Substituição Cirúrgica:** Copiamos esse novo `.exe` para dentro da pasta `src-tauri/binaries` manualmente.
3.  **Build Final:** Rodamos o build do Tauri para empacotar esse novo binário.

### ✅ Estado Atual
- **Master Sender:** Build finalizado com sucesso. Binário atualizado.
- **Client Copier:** Processo de build simétrico realizado para garantir consistência.

---

## 🔜 Próximos Passos (Imediato)
1. Fazer o build final do **Client Copier**.
2. Executar o teste ponta-a-ponta: Abrir ordem no Master -> Verificar cópia no Client.
