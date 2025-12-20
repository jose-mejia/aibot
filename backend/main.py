"""
AI Trading Bot - Backend Principal
FastAPI server para gerenciar o sistema de trading
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api.routes import router
from services.bot_service import BotService

# Instância global do serviço do bot
bot_service = BotService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Startup
    print("🚀 Iniciando AI Trading Bot Backend...")
    yield
    # Shutdown
    print("🛑 Encerrando AI Trading Bot Backend...")
    bot_service.stop()

app = FastAPI(
    title="AI Trading Bot API",
    description="API para controle do sistema de trading automatizado",
    version="1.0.0",
    lifespan=lifespan
)

# CORS para permitir comunicação com frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(router)

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "AI Trading Bot API",
        "status": "running",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

