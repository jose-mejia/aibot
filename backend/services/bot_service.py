"""
Serviço Principal do Bot
Orquestra todos os módulos
"""

import threading
import time
from datetime import datetime
from typing import Dict, List, Optional
from collections import deque
import uuid

from mt5.connector import MT5Connector
from mt5.trade_manager import TradeManager
from core_ai.ai_engine import AIEngine
from storage.database import Database
from models.schemas import BotConfig, Trade, LogEntry, Action

class BotService:
    """Serviço principal que orquestra todos os módulos"""
    
    def __init__(self):
        # Módulos
        self.mt5_connector = MT5Connector()
        self.trade_manager = TradeManager()
        self.ai_engine = AIEngine()
        self.database = Database()
        
        # Estado
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.config = BotConfig()
        
        # Histórico em memória
        self.logs: deque = deque(maxlen=1000)
        self.last_ai_decision: Optional[Dict] = None
    
    def get_status(self) -> Dict:
        """Retorna status do sistema"""
        return {
            "bot_running": self.running,
            "mt5_connected": self.mt5_connector.is_connected(),
            "current_config": self.config.dict(),
            "timestamp": datetime.now().isoformat()
        }
    
    def start(self) -> Dict:
        """Inicia o bot"""
        if self.running:
            return {
                "success": False,
                "message": "Bot já está rodando"
            }
        
        # Validar conexão MT5
        if not self.mt5_connector.is_connected():
            connection = self.mt5_connector.connect()
            if not connection.get("connected"):
                return {
                    "success": False,
                    "message": f"Falha ao conectar MT5: {connection.get('message')}"
                }
        
        # Validar modo DEMO
        if not self.config.demo_mode:
            return {
                "success": False,
                "message": "⚠️ Sistema configurado apenas para conta DEMO!"
            }
        
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        
        self._log("INFO", "🤖 Bot iniciado com sucesso")
        
        return {
            "success": True,
            "message": "Bot iniciado com sucesso"
        }
    
    def stop(self) -> Dict:
        """Para o bot (kill switch)"""
        if not self.running:
            return {
                "success": True,
                "message": "Bot já está parado"
            }
        
        self.running = False
        self._log("INFO", "🛑 Bot parado pelo usuário")
        
        return {
            "success": True,
            "message": "Bot parado com sucesso"
        }
    
    def update_config(self, config_dict: Dict) -> Dict:
        """Atualiza configuração"""
        if self.running:
            return {
                "success": False,
                "message": "Pare o bot antes de alterar configurações"
            }
        
        try:
            self.config = BotConfig(**config_dict)
            self.trade_manager.magic_number = self.config.magic_number
            
            # Salvar configuração no banco
            self.database.save_config("bot_config", self.config.json())
            
            self._log("INFO", f"Configuração atualizada")
            
            return {
                "success": True,
                "message": "Configurações atualizadas",
                "config": self.config.dict()
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }
    
    def get_config(self) -> Dict:
        """Retorna configuração atual"""
        return self.config.dict()
    
    def test_mt5_connection(self) -> Dict:
        """Testa conexão com MT5"""
        result = self.mt5_connector.connect()
        if result.get("connected"):
            self._log("INFO", "Conexão MT5 testada com sucesso")
        else:
            self._log("ERROR", f"Falha na conexão MT5: {result.get('message')}")
        return result
    
    def get_trades(self, limit: int = 50) -> List[Dict]:
        """Retorna trades"""
        return self.database.get_trades(limit=limit, symbol=self.config.symbol)
    
    def get_logs(self, limit: int = 100) -> List[Dict]:
        """Retorna logs"""
        return list(self.logs)[-limit:]
    
    def _run_loop(self):
        """Loop principal de execução do bot"""
        self._log("INFO", "🔄 Loop de execução iniciado")
        
        while self.running:
            try:
                # Verificar conexão MT5
                if not self.mt5_connector.is_connected():
                    self._log("ERROR", "MT5 desconectado. Tentando reconectar...")
                    connection = self.mt5_connector.connect()
                    if not connection.get("connected"):
                        self._log("ERROR", "Falha ao reconectar MT5")
                        time.sleep(10)
                        continue
                
                # Verificar limite de trades simultâneos
                open_positions = self.trade_manager.get_open_positions(
                    symbol=self.config.symbol,
                    magic=self.config.magic_number
                )
                
                if len(open_positions) >= self.config.max_simultaneous_trades:
                    self._log("DEBUG", f"Limite de trades simultâneos atingido ({len(open_positions)})")
                    time.sleep(self.config.analysis_interval)
                    continue
                
                # Coletar dados do mercado
                candles = self.mt5_connector.get_candles(
                    self.config.symbol,
                    self.config.timeframe,
                    count=100
                )
                
                if candles is None or candles.empty:
                    self._log("WARNING", "Não foi possível obter candles")
                    time.sleep(5)
                    continue
                
                # Análise da IA
                decision = self.ai_engine.analyze(candles)
                self.last_ai_decision = decision.dict()
                
                # Salvar decisão no banco
                self.database.save_ai_decision(
                    decision.dict(),
                    self.config.symbol,
                    self.config.timeframe.value
                )
                
                self._log("INFO", f"IA Decision: {decision.action.value} | Confiança: {decision.confidence:.2f} | {decision.reason}")
                
                # Validar decisão
                if decision.action == Action.HOLD:
                    self._log("DEBUG", "IA decidiu HOLD. Aguardando...")
                    time.sleep(self.config.analysis_interval)
                    continue
                
                # Executar ordem se necessário
                if decision.action in [Action.BUY, Action.SELL]:
                    self._execute_trade(decision)
                
                # Aguardar próximo ciclo
                time.sleep(self.config.analysis_interval)
                
            except Exception as e:
                self._log("ERROR", f"Erro no loop de execução: {str(e)}")
                time.sleep(5)
        
        self._log("INFO", "Loop de execução finalizado")
    
    def _execute_trade(self, decision):
        """Executa trade baseado na decisão da IA"""
        try:
            self._log("INFO", f"Executando {decision.action.value} em {self.config.symbol}")
            
            # Executar ordem no MT5
            result = self.trade_manager.place_order(
                symbol=self.config.symbol,
                order_type=decision.action.value,
                volume=self.config.volume,
                stop_loss=self.config.stop_loss,
                take_profit=self.config.take_profit,
                comment=f"AI Bot - {decision.reason[:50]}"
            )
            
            if not result.get("success"):
                self._log("ERROR", f"Falha ao executar ordem: {result.get('message')}")
                return
            
            # Criar registro de trade
            trade = {
                "id": str(uuid.uuid4()),
                "symbol": self.config.symbol,
                "type": decision.action.value,
                "entry_price": result.get("price", 0),
                "volume": self.config.volume,
                "stop_loss": self.config.stop_loss,
                "take_profit": self.config.take_profit,
                "status": "OPEN",
                "open_time": datetime.now().isoformat(),
                "ai_decision_id": None  # Será atualizado depois
            }
            
            # Salvar no banco
            self.database.save_trade(trade)
            
            self._log("INFO", f"✅ Trade executado: {trade['type']} {trade['symbol']} @ {trade['entry_price']}")
            
        except Exception as e:
            self._log("ERROR", f"Erro ao executar trade: {str(e)}")
    
    def _log(self, level: str, message: str, source: str = "BotService"):
        """Registra log"""
        log_entry = {
            "level": level,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "source": source
        }
        self.logs.append(log_entry)
        print(f"[{level}] {message}")

# Instância global
bot_service = BotService()

