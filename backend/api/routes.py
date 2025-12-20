"""
Rotas da API - Endpoints obrigatórios
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from services.bot_service import bot_service
from models.schemas import BotConfig, Trade, LogEntry

router = APIRouter(prefix="/api", tags=["trading"])

@router.get("/status")
async def get_status():
    """Retorna o status atual do sistema"""
    return bot_service.get_status()

@router.post("/bot/start")
async def start_bot():
    """Inicia o robô de trading"""
    try:
        result = bot_service.start()
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bot/stop")
async def stop_bot():
    """Para o robô de trading (kill switch)"""
    try:
        result = bot_service.stop()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/config")
async def update_config(config: BotConfig):
    """Atualiza configurações do bot"""
    try:
        result = bot_service.update_config(config.dict())
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/config")
async def get_config():
    """Retorna configurações atuais"""
    return bot_service.get_config()

@router.get("/trades")
async def get_trades(limit: int = 50):
    """Retorna histórico de trades"""
    try:
        trades = bot_service.get_trades(limit)
        return {
            "trades": trades,
            "count": len(trades),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs")
async def get_logs(limit: int = 100):
    """Retorna logs do sistema"""
    try:
        logs = bot_service.get_logs(limit)
        return {
            "logs": logs,
            "count": len(logs),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mt5/test")
async def test_mt5_connection():
    """Testa conexão com MetaTrader 5"""
    try:
        result = bot_service.test_mt5_connection()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
