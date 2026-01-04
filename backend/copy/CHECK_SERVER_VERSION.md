# Validação da Versão da API

Se você está recebendo **Erro 500** ao salvar o perfil, sua API não está rodando o código mais recente.

## Passos para corrigir:

1.  **Vá ao terminal da API Server.**
2.  Pressione `Ctrl+C` para parar o servidor atual.
3.  Execute o comando para limpar builds antigos (opcional, mas recomendado):
    ```powershell
    cargo clean
    ```
4.  Inicie o servidor novamente:
    ```powershell
    cargo run
    ```
    *Aguarde a recompilação (pode demorar 1-2 minutos).*

## Como saber se funcionou?

Quando você clicar em "Salvar" no Profile, olhe o terminal da API. Você DEVE ver uma mensagem assim:

```text
🔍 UPDATE ME PAYLOAD: UpdateUserReq { ... mt5_path: Some("..."), ... }
```

Se essa mensagem **NÃO APARECER**, o servidor ainda está rodando uma versão antiga.
