# Merged Jobot - Versão Híbrida v7.00

## Visão Geral
Este projeto evoluiu para o **Merged Jobot v7.00**, uma fusão robusta entre um painel visual avançado (TraderHelper) e a estratégia clássica do Oscilador Acelerador (AC). O resultado é um Expert Advisor (EA) profissional com foco em Price Action, segurança de capital e feedback visual em tempo real.

## Estratégia Unificada
O robô combina múltiplos conceitos para tomada de decisão:

1.  **Price Action & Consenso:**
    *   Analisa as últimas velas para determinar a tendência de curto prazo.
    *   Calcula um **Score de Força** (Compra vs Venda) baseado nas máximas e mínimas.
2.  **Filtro de Tendência (SMA):**
    *   Utiliza uma Média Móvel Simples (SMA) para definir o viés primário (Alta/Baixa).
3.  **Filtro Oscilador Acelerador (AC):**
    *   *Novo:* Integração do indicador `iAC`.
    *   Funciona como "pente fino": só opera se o indicador AC confirmar a aceleração do movimento.
    *   **Configurável:** Pode ser ligado/desligado via input `InpUsarAC`.

## Funcionalidades e Painel Visual
O robô desenha um **Dashboard Completo** no gráfico:
*   **Status Box:** Informa se o robô está OPERANDO, PAUSADO (Notícia) ou ENCERRADO (Meta/Loss batido).
*   **Placar Quantitativo:** Mostra o score de agressão de compradores vs vendedores.
*   **Nuvens de Proteção:** Retângulos visuais que indicam zonas de suporte e resistência dinâmicos baseados no D1.
*   **Relógio de Notícias:** Contagem regressiva para eventos configurados.

## Parâmetros de Entrada (Inputs)

### Estratégia
| Parâmetro | Padrão | Descrição |
| :--- | :--- | :--- |
| `InpUsarAC` | `true` | Ativa/Desativa o filtro do Oscilador Acelerador. |
| `InpPeriodoMedia` | `10` | Período da Média Móvel para tendência. |
| `InpPercentualRomp` | `0.15` | % de rompimento da vela anterior para gatilho. |

### Segurança e Risco (Gestão Financeira)
| Parâmetro | Padrão | Descrição |
| :--- | :--- | :--- |
| `InpVolume` | `0.0` | Lote Fixo (0.0 = usa o mínimo da corretora). |
| `InpMaxSpread` | `45` | Spread máximo permitido (pontos) para evitar custos altos. |
| `InpMetaFinanceira` | `50.00` | Meta de Lucas Diária ($). O robô para ao atingir. |
| `InpDrawdownMax` | `100.00` | Perda Máxima Diária ($). O robô trava ao atingir. |
| `InpMaxOperacoes` | `100` | Limite de trades por dia. |

### Filtro de Notícias
| Parâmetro | Padrão | Descrição |
| :--- | :--- | :--- |
| `InpHoraNoticia` | `10:30` | Horário de evento crítico (formatar HH:MM). |
| `InpMinAntes` | `5` | Minutos de pausa antes da notícia. |
| `InpMinDepois` | `5` | Minutos de pausa após a notícia. |

## Validações de Sistema
O robô realiza checagens automáticas constantes:
1.  **Conectividade:** Monitora conexão com o servidor da corretora.
2.  **Margem Livre:** Impede abertura de ordens se a margem for insuficiente.
3.  **Persistência:** Salva o número de operações em variáveis globais para não perder a conta se o MT5 reiniciar.
4.  **Estabilidade:** Aguarda X segundos no início de cada vela antes de operar.

## Instalação
1.  Compile o arquivo `merged_bot.mql5` no MetaEditor.
2.  Arraste para o gráfico (Recomendado: Timeframes menores como M1, M5 ou M15 para escalpelamento, ou H1 para swing).
3.  Verifique se o botão "Algo Trading" do MT5 está verde.
