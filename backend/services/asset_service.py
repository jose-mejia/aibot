"""
Serviço de Gerenciamento de Ativos Monitorados
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

class AssetService:
    """Gerencia ativos monitorados e coleta de dados"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.market_data_dir = os.path.join(data_dir, "market_data")
        self.config_file = os.path.join(data_dir, "monitored_assets.json")
        self._ensure_directories()
        self._initialize_default_assets()
    
    def _ensure_directories(self):
        """Garante que os diretórios existem"""
        os.makedirs(self.market_data_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _initialize_default_assets(self):
        """Inicializa ativos padrão se não existir configuração"""
        if not os.path.exists(self.config_file):
            default_assets = [
                {"symbol": "EURUSD", "active": True, "timeframes": ["H1"], "last_candle_time": None},
                {"symbol": "GBPUSD", "active": True, "timeframes": ["H1"], "last_candle_time": None},
                {"symbol": "USDJPY", "active": True, "timeframes": ["H1"], "last_candle_time": None},
                {"symbol": "USDCHF", "active": True, "timeframes": ["H1"], "last_candle_time": None},
                {"symbol": "BTCUSD", "active": True, "timeframes": ["H1"], "last_candle_time": None},
            ]
            self._save_assets(default_assets)
    
    def get_assets(self) -> List[Dict]:
        """Retorna lista de ativos monitorados"""
        try:
            if not os.path.exists(self.config_file):
                self._initialize_default_assets()
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("assets", [])
        except Exception as e:
            print(f"Erro ao carregar ativos: {e}")
            return []
    
    def update_assets(self, assets: List[Dict]) -> Dict:
        """Atualiza lista de ativos"""
        try:
            # Validar máximo de 5 ativos
            if len(assets) > 5:
                return {
                    "success": False,
                    "message": "Máximo de 5 ativos permitidos"
                }
            
            # Validar símbolos únicos
            symbols = [a["symbol"] for a in assets]
            if len(symbols) != len(set(symbols)):
                return {
                    "success": False,
                    "message": "Símbolos duplicados não são permitidos"
                }
            
            # Criar diretórios para novos ativos
            for asset in assets:
                symbol = asset["symbol"]
                for tf in asset.get("timeframes", ["H1"]):
                    asset_dir = os.path.join(self.market_data_dir, symbol)
                    os.makedirs(asset_dir, exist_ok=True)
            
            # Salvar
            self._save_assets(assets)
            
            return {
                "success": True,
                "message": "Ativos atualizados com sucesso",
                "assets": assets
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao atualizar ativos: {str(e)}"
            }
    
    def _save_assets(self, assets: List[Dict]):
        """Salva lista de ativos"""
        data = {
            "assets": assets,
            "updated_at": datetime.now().isoformat()
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_active_assets(self) -> List[Dict]:
        """Retorna apenas ativos ativos"""
        assets = self.get_assets()
        return [a for a in assets if a.get("active", False)]
    
    def save_candle(self, symbol: str, timeframe: str, candle: Dict) -> bool:
        """
        Salva uma vela no arquivo JSON do ativo
        
        Args:
            symbol: Símbolo do ativo (ex: EURUSD)
            timeframe: Timeframe (ex: H1)
            candle: Dicionário com dados da vela
            
        Returns:
            bool: True se salvou com sucesso
        """
        try:
            asset_dir = os.path.join(self.market_data_dir, symbol)
            os.makedirs(asset_dir, exist_ok=True)
            
            file_path = os.path.join(asset_dir, f"{timeframe}.json")
            
            # Carregar dados existentes
            candles = []
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    candles = json.load(f)
            
            # Verificar se vela já existe (evitar duplicação)
            candle_timestamp = candle.get("timestamp")
            existing_timestamps = [c.get("timestamp") for c in candles]
            
            if candle_timestamp not in existing_timestamps:
                candles.append(candle)
                # Ordenar por timestamp
                candles.sort(key=lambda x: x.get("timestamp", ""))
                
                # Salvar
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(candles, f, indent=2, ensure_ascii=False)
                
                return True
            else:
                # Vela já existe, atualizar
                for i, c in enumerate(candles):
                    if c.get("timestamp") == candle_timestamp:
                        candles[i] = candle
                        break
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(candles, f, indent=2, ensure_ascii=False)
                
                return True
                
        except Exception as e:
            print(f"Erro ao salvar vela: {e}")
            return False
    
    def get_candles(self, symbol: str, timeframe: str, limit: Optional[int] = None) -> List[Dict]:
        """
        Retorna velas salvas de um ativo
        
        Args:
            symbol: Símbolo do ativo
            timeframe: Timeframe
            limit: Limite de velas (None = todas)
            
        Returns:
            Lista de velas
        """
        try:
            file_path = os.path.join(self.market_data_dir, symbol, f"{timeframe}.json")
            
            if not os.path.exists(file_path):
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                candles = json.load(f)
            
            if limit:
                return candles[-limit:]
            
            return candles
        except Exception as e:
            print(f"Erro ao carregar velas: {e}")
            return []
    
    def get_last_candle_time(self, symbol: str, timeframe: str) -> Optional[datetime]:
        """Retorna timestamp da última vela salva"""
        candles = self.get_candles(symbol, timeframe, limit=1)
        if candles:
            timestamp_str = candles[-1].get("timestamp")
            if timestamp_str:
                try:
                    # Tratar diferentes formatos de timestamp
                    ts = timestamp_str.replace('Z', '+00:00')
                    return datetime.fromisoformat(ts)
                except Exception as e:
                    print(f"Erro ao parsear timestamp: {e}")
                    return None
        return None
    
    def update_last_candle_time(self, symbol: str, timeframe: str, timestamp: datetime):
        """Atualiza timestamp da última vela coletada"""
        assets = self.get_assets()
        for asset in assets:
            if asset["symbol"] == symbol:
                asset["last_candle_time"] = timestamp.isoformat()
                break
        self._save_assets(assets)

