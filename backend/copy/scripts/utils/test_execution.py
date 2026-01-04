import MetaTrader5 as mt5
import time

def test_mt5_order():
    if not mt5.initialize():
        print("❌ Falha ao inicializar MT5")
        return

    symbol = "BTCUSD" # Tente mudar se o seu broker usar sufixo, ex: "BTCUSD.a"
    volume = 0.01
    
    # 1. Verificar Símbolo
    print(f"🔍 Verificando símbolo {symbol}...")
    if not mt5.symbol_select(symbol, True):
        print(f"❌ Símbolo {symbol} NÃO encontrado ou não disponível!")
        print("⚠️  Dica: Verifique se o símbolo está visível na Observação do Mercado.")
        print("⚠️  Dica: Seu broker pode usar um sufixo (ex: .m, .a)")
        mt5.shutdown()
        return
    else:
        print(f"✅ Símbolo {symbol} selecionado com sucesso.")

    # 2. Verificar Preço
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"❌ Não foi possível obter preço para {symbol}. Mercado fechado?")
        mt5.shutdown()
        return
    
    print(f"💰 Preço atual (Ask): {tick.ask}")

    # 3. Tentar Ordem de Teste (Buy Stop bem longe para não executar)
    print("🚀 Tentando enviar ordem PENDENTE de teste...")
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY_STOP,
        "price": tick.ask + 1000.0, # Preço bem alto para não executar
        "magic": 123456,
        "comment": "TEST_ORDER",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Falha ao enviar ordem: {result.retcode} - {result.comment}")
    else:
        print(f"✅ Ordem de teste enviada com sucesso! Ticket: {result.order}")
        print("🗑️  Deletando ordem de teste em 3 segundos...")
        time.sleep(3)
        
        # Deletar
        remove_req = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": result.order
        }
        mt5.order_send(remove_req)
        print("✅ Ordem deletada.")

    mt5.shutdown()

if __name__ == "__main__":
    test_mt5_order()
