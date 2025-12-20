"""
Gerenciador de Operações MT5
Responsável por abrir, gerenciar e fechar ordens
"""

import MetaTrader5 as mt5
from datetime import datetime
from typing import Dict, List, Optional
import pytz

class TradeManager:
    """
    Gerenciador de operações
    
    Responsabilidades:
    - Abrir ordens no MT5
    - Gerenciar ordens abertas
    - Evitar múltiplas ordens simultâneas no mesmo par
    - Aplicar regras de risco
    - Fechar operações corretamente
    """
    
    def __init__(self, magic_number: int = 234000):
        self.magic_number = magic_number
    
    def place_order(
        self,
        symbol: str,
        order_type: str,  # "BUY" ou "SELL"
        volume: float,
        stop_loss: float = 0,
        take_profit: float = 0,
        comment: str = "AI Trading Bot"
    ) -> Dict:
        """
        Executa ordem no MT5
        
        Args:
            symbol: Par de moedas
            order_type: "BUY" ou "SELL"
            volume: Volume (lote)
            stop_loss: Preço de stop loss (0 = não usar)
            take_profit: Preço de take profit (0 = não usar)
            comment: Comentário da ordem
            
        Returns:
            Dict com resultado da ordem
        """
        if not mt5.initialize():
            return {
                "success": False,
                "message": "MT5 não está inicializado"
            }
        
        try:
            # Obter informações do símbolo
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                return {
                    "success": False,
                    "message": f"Símbolo {symbol} não encontrado"
                }
            
            # Verificar se símbolo está ativo
            if not symbol_info.visible:
                if not mt5.symbol_select(symbol, True):
                    return {
                        "success": False,
                        "message": f"Falha ao ativar símbolo {symbol}"
                    }
            
            # Preparar ordem
            point = symbol_info.point
            tick = mt5.symbol_info_tick(symbol)
            
            if order_type == "BUY":
                order_type_mt5 = mt5.ORDER_TYPE_BUY
                price = tick.ask
                sl = price - stop_loss * point if stop_loss > 0 else 0
                tp = price + take_profit * point if take_profit > 0 else 0
            else:  # SELL
                order_type_mt5 = mt5.ORDER_TYPE_SELL
                price = tick.bid
                sl = price + stop_loss * point if stop_loss > 0 else 0
                tp = price - take_profit * point if take_profit > 0 else 0
            
            # Validar SL e TP (obrigatório)
            if stop_loss <= 0 or take_profit <= 0:
                return {
                    "success": False,
                    "message": "Stop Loss e Take Profit são obrigatórios"
                }
            
            # Criar request
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type_mt5,
                "price": price,
                "sl": sl,
                "tp": tp,
                "deviation": 20,
                "magic": self.magic_number,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # Enviar ordem
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                return {
                    "success": False,
                    "message": f"Falha ao executar ordem: {result.comment}",
                    "retcode": result.retcode
                }
            
            return {
                "success": True,
                "message": "Ordem executada com sucesso",
                "order_id": result.order,
                "deal_id": result.deal,
                "volume": result.volume,
                "price": result.price,
                "comment": result.comment
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao executar ordem: {str(e)}"
            }
    
    def get_open_positions(self, symbol: Optional[str] = None, magic: Optional[int] = None) -> List[Dict]:
        """
        Obtém posições abertas
        
        Args:
            symbol: Filtrar por símbolo (None = todas)
            magic: Filtrar por magic number (None = todas)
            
        Returns:
            Lista de posições abertas
        """
        if not mt5.initialize():
            return []
        
        try:
            positions = mt5.positions_get(symbol=symbol) if symbol else mt5.positions_get()
            
            if positions is None:
                return []
            
            result = []
            for pos in positions:
                # Filtrar por magic number se especificado
                if magic is not None and pos.magic != magic:
                    continue
                
                result.append({
                    "ticket": pos.ticket,
                    "symbol": pos.symbol,
                    "type": "BUY" if pos.type == mt5.ORDER_TYPE_BUY else "SELL",
                    "volume": pos.volume,
                    "price_open": pos.price_open,
                    "price_current": pos.price_current,
                    "stop_loss": pos.sl,
                    "take_profit": pos.tp,
                    "profit": pos.profit,
                    "swap": pos.swap,
                    "comment": pos.comment,
                    "magic": pos.magic,
                    "time": datetime.fromtimestamp(pos.time, tz=pytz.UTC)
                })
            
            return result
            
        except Exception as e:
            print(f"Erro ao obter posições: {e}")
            return []
    
    def close_position(self, ticket: int) -> Dict:
        """
        Fecha uma posição
        
        Args:
            ticket: Ticket da posição
            
        Returns:
            Dict com resultado
        """
        if not mt5.initialize():
            return {
                "success": False,
                "message": "MT5 não está inicializado"
            }
        
        try:
            # Obter informações da posição
            position = mt5.positions_get(ticket=ticket)
            if position is None or len(position) == 0:
                return {
                    "success": False,
                    "message": "Posição não encontrada"
                }
            
            pos = position[0]
            
            # Preparar ordem de fechamento
            tick = mt5.symbol_info_tick(pos.symbol)
            price = tick.bid if pos.type == mt5.ORDER_TYPE_BUY else tick.ask
            
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
                "position": ticket,
                "price": price,
                "deviation": 20,
                "magic": self.magic_number,
                "comment": "AI Bot Close",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                return {
                    "success": False,
                    "message": f"Falha ao fechar posição: {result.comment}",
                    "retcode": result.retcode
                }
            
            return {
                "success": True,
                "message": "Posição fechada com sucesso",
                "order_id": result.order,
                "deal_id": result.deal
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao fechar posição: {str(e)}"
            }
    
    def count_open_positions(self, symbol: str, magic: Optional[int] = None) -> int:
        """Conta posições abertas para um símbolo"""
        return len(self.get_open_positions(symbol=symbol, magic=magic))

