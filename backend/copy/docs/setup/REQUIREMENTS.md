# Requirements - Dependências Python

## Dependências de Produção

```txt
# Core MT5
MetaTrader5==5.0.5430

# Numpy - VERSÃO CRÍTICA
numpy>=1.26.0,<2.0

# HTTP Client
requests==2.32.5

# Autenticação
python-jose==3.5.0
passlib==1.7.4
bcrypt==5.0.0

# Utilitários
python-dotenv==1.2.1
```

## Dependências de Build

```txt
# Empacotamento
pyinstaller==6.17.0
pyinstaller-hooks-contrib>=2025.11

# Utilitários de build
pefile==2024.8.26
```

## Dependências de Desenvolvimento

```txt
# Testing
pytest==8.3.4
pytest-asyncio==0.25.2
pytest-cov==6.0.0

# Linting
flake8==7.1.1
black==25.1.0
mypy==1.15.0

# Type stubs
types-requests==2.32.0
```

## Instalação

### Produção
```bash
pip install -r requirements.txt
```

### Desenvolvimento
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Notas Importantes

### ⚠️ Numpy

**NUNCA use numpy 2.x!**

Motivo: Incompatibilidade com MetaTrader5 e PyInstaller.

Se acidentalmente instalou numpy 2.x:
```bash
pip uninstall numpy -y
pip install "numpy<2"
```

### Python Version

Este projeto requer **Python 3.12.x**.

Versões testadas:
- ✅ Python 3.12.0
- ✅ Python 3.12.1
- ✅ Python 3.12.7

Versões não suportadas:
- ❌ Python 3.11.x (falta de features)
- ❌ Python 3.13.x (não testado)

### Windows Only

MetaTrader5 Python API só funciona em **Windows**.

Não há suporte para Linux/macOS.
