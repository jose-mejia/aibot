"""
Armazenamento Local - SQLite
Gerencia persistência de dados para aprendizado da IA
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import os

class Database:
    """
    Gerenciador de banco de dados local
    
    Armazena:
    - Histórico de candles
    - Decisões da IA
    - Resultados de trades
    - Configurações
    """
    
    def __init__(self, db_path: str = "data/trading_bot.db"):
        self.db_path = db_path
        self._ensure_data_dir()
        self._init_database()
    
    def _ensure_data_dir(self):
        """Garante que o diretório de dados existe"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _init_database(self):
        """Inicializa o banco de dados e cria tabelas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de decisões da IA
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action TEXT NOT NULL,
                confidence REAL NOT NULL,
                reason TEXT,
                indicators TEXT,
                symbol TEXT,
                timeframe TEXT
            )
        """)
        
        # Tabela de trades
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id TEXT PRIMARY KEY,
                symbol TEXT NOT NULL,
                type TEXT NOT NULL,
                entry_price REAL NOT NULL,
                exit_price REAL,
                volume REAL NOT NULL,
                stop_loss REAL NOT NULL,
                take_profit REAL NOT NULL,
                profit REAL,
                status TEXT NOT NULL,
                open_time TEXT NOT NULL,
                close_time TEXT,
                ai_decision_id INTEGER,
                FOREIGN KEY (ai_decision_id) REFERENCES ai_decisions(id)
            )
        """)
        
        # Tabela de candles (para histórico)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS candles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                timeframe TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                open REAL NOT NULL,
                high REAL NOT NULL,
                low REAL NOT NULL,
                close REAL NOT NULL,
                volume INTEGER NOT NULL,
                UNIQUE(symbol, timeframe, timestamp)
            )
        """)
        
        # Tabela de configurações
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_ai_decision(self, decision: Dict, symbol: str, timeframe: str) -> int:
        """Salva decisão da IA"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO ai_decisions 
            (timestamp, action, confidence, reason, indicators, symbol, timeframe)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            decision["timestamp"],
            decision["action"],
            decision["confidence"],
            decision["reason"],
            json.dumps(decision.get("indicators", {})),
            symbol,
            timeframe
        ))
        
        decision_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return decision_id
    
    def save_trade(self, trade: Dict) -> bool:
        """Salva trade"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO trades 
                (id, symbol, type, entry_price, exit_price, volume, stop_loss, take_profit,
                 profit, status, open_time, close_time, ai_decision_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                trade["id"],
                trade["symbol"],
                trade["type"],
                trade["entry_price"],
                trade.get("exit_price"),
                trade["volume"],
                trade["stop_loss"],
                trade["take_profit"],
                trade.get("profit"),
                trade["status"],
                trade["open_time"],
                trade.get("close_time"),
                trade.get("ai_decision_id")
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao salvar trade: {e}")
            conn.close()
            return False
    
    def get_trades(self, limit: int = 50, symbol: Optional[str] = None) -> List[Dict]:
        """Obtém trades"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM trades"
        params = []
        
        if symbol:
            query += " WHERE symbol = ?"
            params.append(symbol)
        
        query += " ORDER BY open_time DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        trades = []
        for row in rows:
            trades.append(dict(row))
        
        conn.close()
        return trades
    
    def get_ai_decisions(self, limit: int = 100) -> List[Dict]:
        """Obtém decisões da IA"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM ai_decisions 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        decisions = []
        for row in rows:
            decision = dict(row)
            # Parse indicators JSON
            if decision.get("indicators"):
                decision["indicators"] = json.loads(decision["indicators"])
            decisions.append(decision)
        
        conn.close()
        return decisions
    
    def save_config(self, key: str, value: str):
        """Salva configuração"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO config (key, value, updated_at)
            VALUES (?, ?, ?)
        """, (key, value, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_config(self, key: str) -> Optional[str]:
        """Obtém configuração"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT value FROM config WHERE key = ?", (key,))
        row = cursor.fetchone()
        
        conn.close()
        return row[0] if row else None

