# Guia de Teste - Executáveis do Trade Copier

## 📦 Gerando os Executáveis

Para criar os arquivos `.exe` de teste, execute:

```bash
build_test_exe.bat
```

Este script irá:
1. Instalar as dependências necessárias
2. Compilar o **Master Sender** (`master_sender.exe`)
3. Compilar o **Client Copier** (`client_copier.exe`)
4. Copiar os arquivos de configuração
5. Colocar tudo na pasta `dist_test/`

## 🔧 Configuração

### 1. Configurar o Master Sender

Edite `dist_test/config_sender.json`:

```json
{
  "api_url": "http://localhost:8080",
  "api_key": "sua_api_key_aqui",
  "mt5": {
    "login": 12345678,
    "password": "sua_senha",
    "server": "seu_servidor_mt5"
  }
}
```

### 2. Configurar o Client Copier

Edite `dist_test/config_client.json`:

```json
{
  "api_url": "http://localhost:8080",
  "api_key": "sua_api_key_aqui",
  "mt5": {
    "login": 87654321,
    "password": "sua_senha",
    "server": "seu_servidor_mt5"
  },
  "websocket_url": "ws://localhost:8080/ws"
}
```

## 🚀 Testando a Integração

### Passo 1: Iniciar o Servidor API (Rust)

Primeiro, certifique-se de que o servidor Rust está rodando:

```bash
cd api_server
cargo run --release
```

O servidor deve iniciar em `http://localhost:8080`

### Passo 2: Iniciar o Master Sender

Abra um terminal e execute:

```bash
cd dist_test
master_sender.exe
```

O Master Sender irá:
- Conectar ao MT5 da conta Master
- Monitorar ordens abertas
- Enviar atualizações para o servidor API

### Passo 3: Iniciar o Client Copier

Abra outro terminal e execute:

```bash
cd dist_test
client_copier.exe
```

O Client Copier irá:
- Conectar ao MT5 da conta Client
- Conectar ao WebSocket do servidor
- Receber e copiar ordens do Master

## 📊 Verificando a Integração

### Logs

Ambos os executáveis geram logs:
- `sender.log` - logs do Master Sender
- `client.log` - logs do Client Copier

### Teste Básico

1. **Abra uma ordem no MT5 Master**
   - Exemplo: Comprar 0.01 lote de EURUSD

2. **Verifique o Master Sender**
   - Deve detectar a nova ordem
   - Deve enviar para o servidor API
   - Log deve mostrar: `"Order sent to API: ..."`

3. **Verifique o Client Copier**
   - Deve receber a ordem via WebSocket
   - Deve copiar a ordem no MT5 Client
   - Log deve mostrar: `"Order copied: ..."`

4. **Verifique o MT5 Client**
   - Deve ter uma ordem idêntica aberta

## 🐛 Troubleshooting

### Master Sender não conecta

- Verifique se o MT5 está aberto e logado
- Verifique as credenciais em `config_sender.json`
- Verifique se o servidor API está rodando

### Client Copier não recebe ordens

- Verifique se o WebSocket está configurado corretamente
- Verifique se o Master Sender está enviando ordens
- Verifique os logs do servidor API

### Erro de compilação

- Certifique-se de ter Python instalado
- Execute: `pip install --upgrade pyinstaller`
- Tente limpar e recompilar:
  ```bash
  rmdir /s /q master_sender\dist
  rmdir /s /q master_sender\build
  rmdir /s /q client_copier\dist
  rmdir /s /q client_copier\build
  build_test_exe.bat
  ```

## 🔄 Argumentos de Linha de Comando

Você pode sobrescrever o ID do MT5 via CLI:

```bash
# Master com ID diferente
master_sender.exe --mt5-id 99999999

# Client com ID diferente
client_copier.exe --mt5-id 88888888
```

## 📝 Próximos Passos

Após validar a integração básica:

1. **Teste com múltiplos clientes** - Execute vários `client_copier.exe` simultaneamente
2. **Teste de failover** - Pare e reinicie componentes para verificar reconexão
3. **Teste de performance** - Abra múltiplas ordens rapidamente
4. **Build com GUI** - Use `build_release.bat` para compilar com interface Tauri

## 🛡️ Segurança

⚠️ **IMPORTANTE**: Os executáveis de teste usam `--console` para facilitar debug. Para produção:
- Use `build_release.bat` que gera executáveis com proteção
- Use `--windowed` ao invés de `--console`
- Proteja suas API keys e credenciais MT5

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs (`sender.log` e `client.log`)
2. Verifique os logs do servidor Rust
3. Teste cada componente individualmente
