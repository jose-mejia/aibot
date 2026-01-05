# 📋 Índice de Erros e Soluções

Este diretório contém documentação de troubleshooting para o Zulfinance Trade Copier.

## 📚 Documentos Disponíveis

### [COMMON_ISSUES.md](./COMMON_ISSUES.md)
Erros mais frequentes e suas soluções, organizados por categoria:

1. **Conexão MT5 e Build**
   - ❌ "Wrong Account!" mesmo configurado corretamente
   - ❌ "Python Sidecar Failed to Start"
   - ❌ "ModuleNotFoundError: No module named 'numpy'"
   - ❌ "ImportError: numpy._core.multiarray failed to import"

2. **Configuração e Paths**
   - ❌ "Config file not found"
   - ❌ MT5 Path inválido

3. **Banco de Dados**
   - ❌ Erro de conexão SQLite
   - ❌ Tabelas não encontradas

4. **API e Autenticação**
   - ❌ Token inválido
   - ❌ HMAC signature mismatch

## 🔍 Como Usar

1. **Identifique o erro** nos logs do aplicativo
2. **Busque a seção** correspondente em `COMMON_ISSUES.md`
3. **Siga o diagnóstico** para confirmar a causa
4. **Aplique a solução** documentada
5. **Valide** que o erro foi resolvido

## 🆘 Erro Não Documentado?

Se encontrar um erro não documentado:

1. Documente no `docs/team/brain_*/BRAIN_DUMP.md` do dia
2. Adicione à seção apropriada de `COMMON_ISSUES.md`
3. Commit com mensagem: `docs(troubleshooting): add solution for [erro]`

## 📖 Documentação Relacionada

- [BUILD_PROCESS.md](../team/BUILD_PROCESS.md) - Processo de build robusto
- [BRAIN_DUMP.md](../team/brain_002/2026-01-05_BRAIN_DUMP.md) - Aprendizados diários
- [DONT.md](../team/DONT.md) - O que NÃO fazer
- [DO.md](../team/DO.md) - Melhores práticas
