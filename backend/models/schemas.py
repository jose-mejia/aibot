"""
Modelos Pydantic para validação de dados
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from enum import Enum

class Timeframe(str, Enum):
    """Timeframes suportados"""
    M1 = "M1"
    M5 = "M5"
    M15 = "M15"
    M30 = "M30"
    H1 = "H1"

class Action(str, Enum):
    """Ações da IA"""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class BotConfig(BaseModel):
    """Configurações do bot"""
    symbol: str = Field(default="EURUSD", description="Par de moedas")
    timeframe: Timeframe = Field(default=Timeframe.M15, description="Timeframe de análise")
    volume: float = Field(default=0.01, ge=0.01, le=100, description="Volume (lote)")
    stop_loss: int = Field(default=50, ge=10, description="Stop Loss em pontos")
    take_profit: int = Field(default=100, ge=10, description="Take Profit em pontos")
    magic_number: int = Field(default=234000, description="Magic Number")
    max_simultaneous_trades: int = Field(default=1, ge=1, le=10, description="Máximo de trades simultâneos")
    analysis_interval: int = Field(default=60, ge=10, description="Intervalo de análise em segundos")
    demo_mode: bool = Field(default=True, description="Modo DEMO (obrigatório)")

class AIDecision(BaseModel):
    """Decisão da IA"""
    action: Action
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str
    timestamp: datetime
    indicators: Optional[dict] = None

class Trade(BaseModel):
    """Trade executado"""
    id: str
    symbol: str
    type: Literal["BUY", "SELL"]
    entry_price: float
    exit_price: Optional[float] = None
    volume: float
    stop_loss: float
    take_profit: float
    profit: Optional[float] = None
    status: Literal["OPEN", "CLOSED", "CANCELLED"]
    open_time: datetime
    close_time: Optional[datetime] = None
    ai_decision: Optional[dict] = None

class LogEntry(BaseModel):
    """Entrada de log"""
    level: Literal["INFO", "WARNING", "ERROR", "DEBUG"]
    message: str
    timestamp: datetime
    source: Optional[str] = None
