"""
Coletor de Velas - Gerencia coleta automática de dados
Garante que apenas velas fechadas sejam coletadas
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import pytz
from mt5.connector import MT5Connector
from models.schemas import Timeframe
from services.asset_service import AssetService

class CandleCollector:
    """
    Coletor de velas com controle de timestamp
    Garante que apenas velas fechadas sejam coletadas
    """
    
    def __init__(self, mt5_connector: MT5Connector, asset_service: AssetService):
        self.mt5 = mt5_connector
        self.asset_service = asset_service
        self.timeframe_minutes = {
            "M1": 1,
            "M5": 5,
            "M15": 15,
            "M30": 30,
            "H1": 60,
            "H4": 240,
            "D1": 1440
        }
    
    def should_collect_candle(self, symbol: str, timeframe: str) -> Tuple[bool, Optional[str]]:
        """
        Verifica se deve coletar uma nova vela
        
        Args:
            symbol: Símbolo do ativo
            timeframe: Timeframe (ex: H1)
            
        Returns:
            (deve_coletar, motivo)
        """
        try:
            # Obter última vela coletada
            last_candle_time = self.asset_service.get_last_candle_time(symbol, timeframe)
            
            # Calcular próximo timestamp esperado
            minutes = self.timeframe_minutes.get(timeframe, 60)
            now = datetime.now(pytz.UTC)
            
            if last_candle_time:
                # Calcular quando a próxima vela deve estar disponível
                next_expected_time = last_candle_time + timedelta(minutes=minutes)
                
                # Só coletar se já passou o tempo necessário
                if now < next_expected_time:
                    remaining = (next_expected_time - now).total_seconds() / 60
                    return False, f"Aguardando fechamento da vela. Restam {remaining:.1f} minutos"
                
                return True, "Vela fechada disponível"
            else:
                # Primeira coleta
                return True, "Primeira coleta"
                
        except Exception as e:
            return False, f"Erro ao verificar: {str(e)}"
    
    def collect_closed_candle(self, symbol: str, timeframe: str) -> Dict:
        """
        Coleta apenas a última vela fechada
        
        Args:
            symbol: Símbolo do ativo
            timeframe: Timeframe
            
        Returns:
            Dict com resultado da coleta
        """
        try:
            # Verificar se deve coletar
            should_collect, reason = self.should_collect_candle(symbol, timeframe)
            
            if not should_collect:
                return {
                    "success": False,
                    "message": reason,
                    "collected": False
                }
            
            # Mapear timeframe
            tf_map = {
                "M1": Timeframe.M1,
                "M5": Timeframe.M5,
                "M15": Timeframe.M15,
                "M30": Timeframe.M30,
                "H1": Timeframe.H1,
            }
            
            mt5_timeframe = tf_map.get(timeframe)
            if not mt5_timeframe:
                return {
                    "success": False,
                    "message": f"Timeframe {timeframe} não suportado",
                    "collected": False
                }
            
            # Coletar apenas 1 vela (a última fechada)
            candles_df = self.mt5.get_candles(symbol, mt5_timeframe, count=1)
            
            if candles_df is None or candles_df.empty:
                return {
                    "success": False,
                    "message": "Não foi possível obter candles do MT5",
                    "collected": False
                }
            
            # Pegar última vela (que já está fechada)
            last_candle = candles_df.iloc[-1]
            
            # Converter timestamp para ISO format
            candle_timestamp = last_candle.name
            if hasattr(candle_timestamp, 'isoformat'):
                timestamp_str = candle_timestamp.isoformat()
            elif hasattr(candle_timestamp, 'strftime'):
                timestamp_str = candle_timestamp.strftime('%Y-%m-%dT%H:%M:%S%z')
            else:
                timestamp_str = str(candle_timestamp)
            
            # Converter para formato JSON
            candle_data = {
                "timestamp": timestamp_str,
                "open": float(last_candle['open']),
                "high": float(last_candle['high']),
                "low": float(last_candle['low']),
                "close": float(last_candle['close']),
                "volume": int(last_candle['volume']) if 'volume' in last_candle else 0
            }
            
            # Salvar vela
            saved = self.asset_service.save_candle(symbol, timeframe, candle_data)
            
            if saved:
                # Atualizar timestamp da última coleta
                try:
                    ts = candle_data["timestamp"].replace('Z', '+00:00')
                    candle_time = datetime.fromisoformat(ts)
                    self.asset_service.update_last_candle_time(symbol, timeframe, candle_time)
                except Exception as e:
                    print(f"Erro ao atualizar timestamp: {e}")
                
                return {
                    "success": True,
                    "message": "Vela coletada e salva com sucesso",
                    "collected": True,
                    "candle": candle_data
                }
            else:
                return {
                    "success": False,
                    "message": "Erro ao salvar vela",
                    "collected": False
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao coletar vela: {str(e)}",
                "collected": False
            }
    
    def collect_all_active_assets(self) -> Dict:
        """
        Coleta velas de todos os ativos ativos
        
        Returns:
            Dict com resultado da coleta
        """
        results = {
            "success": True,
            "collected": 0,
            "skipped": 0,
            "errors": 0,
            "details": []
        }
        
        active_assets = self.asset_service.get_active_assets()
        
        for asset in active_assets:
            symbol = asset["symbol"]
            timeframes = asset.get("timeframes", ["H1"])
            
            for timeframe in timeframes:
                result = self.collect_closed_candle(symbol, timeframe)
                
                if result.get("collected"):
                    results["collected"] += 1
                    results["details"].append({
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "status": "collected"
                    })
                elif result.get("success") == False and "Aguardando" in result.get("message", ""):
                    results["skipped"] += 1
                    results["details"].append({
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "status": "skipped",
                        "reason": result.get("message")
                    })
                else:
                    results["errors"] += 1
                    results["details"].append({
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "status": "error",
                        "reason": result.get("message")
                    })
        
        return results

