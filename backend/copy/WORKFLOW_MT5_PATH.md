# Workflow: Implementação de Caminho Dinâmico MT5

Este workflow guia a implementação da funcionalidade que permite ao usuário configurar o caminho do executável MT5 via interface, resolvendo conflitos de múltiplas instâncias.

## Fases
- [ ] Fase 1: Banco de Dados (Adicionar coluna `mt5_path`)
- [ ] Fase 2: API Rust (Suporte a leitura/escrita de `mt5_path`)
- [ ] Fase 3: Frontend (Input de caminho na UI)
- [ ] Fase 4: Python (Uso do caminho na conexão)

## Detalhes Técnicos
O MT5 Python API requer o argumento `path="..."` no `initialize()` para selecionar uma instância específica quando há múltiplas abertas.

## Instruções de Git
A cada fase completada, realizar commit e push:
- DB: `feat(db): Add mt5_path column`
- API: `feat(api): Support mt5_path in user config`
- Front: `feat(ui): Add MT5 Path input field`
- Bot: `feat(bot): Use dynamic MT5 Path from server`
