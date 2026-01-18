# ⚙️ Mapa de Configurações do Client Copier (Final)

Este documento define os campos de configuração para integração Backend <-> Frontend.

---

## 🚀 1. Configurações de Negócio (Frontend)

Estes campos devem ser expostos na interface de configuração do Robô de Cópia.

### A. Controle de Execução (Latência)
| Campo JSON | Tipo | Padrão | Descrição |
| :--- | :--- | :--- | :--- |
| `max_delay_ms` | `integer` | **3000** | Tolerância máxima de atraso (ms). |

### B. Gestão de Risco (Safety)
| Campo JSON | Tipo | Padrão | Descrição |
| :--- | :--- | :--- | :--- |
| `max_orders_per_symbol` | `integer` | **3** | Limite de ordens por par. |
| `max_lot_per_order` | `float` | **0.10** | Teto de lote por ordem. |
| `max_slippage_points` | `integer` | **50** | Slippage máximo. |
| `max_spread_points` | `integer` | **20** | Spread máximo de entrada. |

### C. Money Management
| Campo JSON | Tipo | Padrão | Descrição |
| :--- | :--- | :--- | :--- |
| `mode` | `string` | **"identical"** | Modos: `identical`, `fixed`. |
| `fixed_lot` | `float` | **0.01** | Valor do lote fixo (se mode=fixed). |

---

## � 2. Configurações de Infraestrutura (Backend/Admin)

Estes campos são gerenciados internamente ou via Banco de Dados Admin, e **NÃO** devem ser alterados pelo usuário final na interface do robô.

| Campo | Origem | Descrição |
| :--- | :--- | :--- |
| `mt5.login` | **API Server** (`/users/me`) | ID da conta MT5 autorizada. |
| `mt5.path` | **API Server** (`/users/me`) | Caminho do executável MT5. |
| `api.url` | **Config/Env** | URL da API REST. |
| `api.ws_url` | **Config/Env** | URL do WebSocket. |
| `magic_number` | **Config Code** | Identificador interno das ordens (padrão 123456). |

---

## 📋 Exemplo de JSON (Frontend Payload)

O frontend deve enviar ou salvar este JSON no arquivo `config_client.json`:

```json
{
    "latency": {
        "max_delay_ms": 3000
    },
    "trade_copy": {
        "mode": "identical", 
        "fixed_lot": 0.01,
        "max_lot_per_order": 0.10,
        "magic_number_copier": 123456
    },
    "safety": {
        "max_orders_per_symbol": 3,
        "max_slippage_points": 50,
        "max_spread_points": 20
    }
}
```
