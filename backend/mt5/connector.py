"""
Conector MetaTrader 5
Gerencia conexão e operações com MT5
"""

import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from typing import Optional, Dict, List
from models.schemas import Timeframe
import pytz

class MT5Connector:
    """Gerenciador de conexão e operações MT5"""
    
    def __init__(self):
        self.connected = False
        self.account_info = None
    
    def connect(self) -> Dict:
        """
        Conecta ao MetaTrader 5
        
        Returns:
            Dict com status da conexão
        """
        try:
            # Inicializar MT5
            if not mt5.initialize():
                error = mt5.last_error()
                return {
                    "success": False,
                    "connected": False,
                    "message": f"Falha ao inicializar MT5: {error}",
                    "details": error
                }
            
            # Verificar informações da conta
            account_info = mt5.account_info()
            if account_info is None:
                mt5.shutdown()
                return {
                    "success": False,
                    "connected": False,
                    "message": "Não foi possível obter informações da conta"
                }
            
            # Validar que é conta DEMO
            if account_info.trade_mode != mt5.ACCOUNT_TRADE_MODE_DEMO:
                return {
                    "success": False,
                    "connected": False,
                    "message": "⚠️ ATENÇÃO: Sistema configurado apenas para conta DEMO!",
                    "account_mode": account_info.trade_mode
                }
            
            self.connected = True
            self.account_info = account_info
            
            return {
                "success": True,
                "connected": True,
                "message": "Conectado ao MT5 com sucesso",
                "account_info": {
                    "login": account_info.login,
                    "server": account_info.server,
                    "balance": account_info.balance,
                    "equity": account_info.equity,
                    "margin": account_info.margin,
                    "free_margin": account_info.margin_free,
                    "trade_mode": "DEMO" if account_info.trade_mode == mt5.ACCOUNT_TRADE_MODE_DEMO else "REAL"
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "connected": False,
                "message": f"Erro ao conectar: {str(e)}"
            }
    
    def disconnect(self):
        """Desconecta do MT5"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            self.account_info = None
    
    def is_connected(self) -> bool:
        """Verifica se está conectado"""
        return self.connected and mt5.initialize()
    
    def get_candles(self, symbol: str, timeframe: Timeframe, count: int = 100) -> Optional[pd.DataFrame]:
        """
        Obtém candles históricos
        
        Args:
            symbol: Par de moedas (ex: EURUSD)
            timeframe: Timeframe (M1, M5, M15, etc)
            count: Número de candles
            
        Returns:
            DataFrame com OHLCV ou None em caso de erro
        """
        if not self.is_connected():
            return None
        
        try:
            # Mapear timeframe
            tf_map = {
                Timeframe.M1: mt5.TIMEFRAME_M1,
                Timeframe.M5: mt5.TIMEFRAME_M5,
                Timeframe.M15: mt5.TIMEFRAME_M15,
                Timeframe.M30: mt5.TIMEFRAME_M30,
                Timeframe.H1: mt5.TIMEFRAME_H1,
            }
            
            mt5_timeframe = tf_map.get(timeframe, mt5.TIMEFRAME_M15)
            
            # Obter candles
            rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, count)
            
            if rates is None or len(rates) == 0:
                return None
            
            # Converter para DataFrame
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)
            
            # Renomear colunas para minúsculas
            df.rename(columns={
                'open': 'open',
                'high': 'high',
                'low': 'low',
                'close': 'close',
                'tick_volume': 'volume'
            }, inplace=True)
            
            return df[['open', 'high', 'low', 'close', 'volume']]
            
        except Exception as e:
            print(f"Erro ao obter candles: {e}")
            return None
    
    def get_current_price(self, symbol: str) -> Optional[Dict]:
        """
        Obtém preço atual do símbolo
        
        Returns:
            Dict com bid, ask, spread ou None
        """
        if not self.is_connected():
            return None
        
        try:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                return None
            
            return {
                "bid": tick.bid,
                "ask": tick.ask,
                "spread": tick.ask - tick.bid,
                "time": datetime.fromtimestamp(tick.time, tz=pytz.UTC)
            }
        except Exception as e:
            print(f"Erro ao obter preço atual: {e}")
            return None
