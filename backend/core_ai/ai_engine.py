"""
Core de Inteligência Artificial - Módulo Desacoplado
Analisa dados e retorna decisões sem executar ordens
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Optional
from models.schemas import Action, AIDecision
import ta

class AIEngine:
    """
    Motor de IA para análise de mercado
    
    Responsabilidades:
    - Receber dados de mercado
    - Calcular indicadores técnicos
    - Tomar decisões baseadas em regras
    - Retornar decisões estruturadas
    
    NÃO executa ordens - apenas retorna decisões
    """
    
    def __init__(self):
        # Parâmetros de análise
        self.rsi_period = 14
        self.ma_fast = 9
        self.ma_slow = 21
        self.macd_fast = 12
        self.macd_slow = 26
        self.macd_signal = 9
    
    def analyze(self, candles: pd.DataFrame) -> AIDecision:
        """
        Analisa o mercado e retorna decisão da IA
        
        Args:
            candles: DataFrame com OHLCV (Open, High, Low, Close, Volume)
            
        Returns:
            AIDecision: Decisão da IA com ação, confiança e motivo
        """
        if candles.empty or len(candles) < 50:
            return AIDecision(
                action=Action.HOLD,
                confidence=0.0,
                reason="Dados insuficientes para análise",
                timestamp=datetime.now()
            )
        
        # Calcular indicadores técnicos
        indicators = self._calculate_indicators(candles)
        
        # Análise baseada em regras
        action, confidence, reason = self._rule_based_analysis(candles, indicators)
        
        # Criar decisão
        decision = AIDecision(
            action=action,
            confidence=confidence,
            reason=reason,
            timestamp=datetime.now(),
            indicators=indicators
        )
        
        return decision
    
    def _calculate_indicators(self, df: pd.DataFrame) -> Dict:
        """Calcula indicadores técnicos"""
        indicators = {}
        
        try:
            # RSI
            indicators['rsi'] = float(ta.momentum.RSIIndicator(df['close'], window=self.rsi_period).rsi().iloc[-1])
            
            # Médias Móveis
            indicators['ma_fast'] = float(df['close'].rolling(window=self.ma_fast).mean().iloc[-1])
            indicators['ma_slow'] = float(df['close'].rolling(window=self.ma_slow).mean().iloc[-1])
            
            # MACD
            macd = ta.trend.MACD(
                df['close'],
                window_fast=self.macd_fast,
                window_slow=self.macd_slow,
                window_sign=self.macd_signal
            )
            indicators['macd'] = float(macd.macd().iloc[-1])
            indicators['macd_signal'] = float(macd.macd_signal().iloc[-1])
            indicators['macd_diff'] = float(macd.macd_diff().iloc[-1])
            
            # Preço atual
            indicators['current_price'] = float(df['close'].iloc[-1])
            indicators['price_change'] = float(((df['close'].iloc[-1] - df['close'].iloc[-2]) / df['close'].iloc[-2]) * 100)
            
            # Volume
            if 'volume' in df.columns:
                indicators['volume_avg'] = float(df['volume'].rolling(window=20).mean().iloc[-1])
                indicators['volume_current'] = float(df['volume'].iloc[-1])
            
        except Exception as e:
            print(f"Erro ao calcular indicadores: {e}")
        
        return indicators
    
    def _rule_based_analysis(self, df: pd.DataFrame, indicators: Dict) -> tuple:
        """
        Análise baseada em regras
        
        Retorna: (action, confidence, reason)
        """
        reasons = []
        buy_score = 0
        sell_score = 0
        
        # RSI Analysis
        rsi = indicators.get('rsi', 50)
        if rsi < 30:
            buy_score += 2
            reasons.append("RSI oversold")
        elif rsi > 70:
            sell_score += 2
            reasons.append("RSI overbought")
        elif 30 <= rsi <= 50:
            buy_score += 1
            reasons.append("RSI neutro-baixo")
        elif 50 < rsi <= 70:
            sell_score += 1
            reasons.append("RSI neutro-alto")
        
        # Moving Average Crossover
        ma_fast = indicators.get('ma_fast', 0)
        ma_slow = indicators.get('ma_slow', 0)
        current_price = indicators.get('current_price', 0)
        
        if ma_fast > ma_slow:
            buy_score += 2
            reasons.append("MA Fast acima de MA Slow (tendência de alta)")
        else:
            sell_score += 2
            reasons.append("MA Fast abaixo de MA Slow (tendência de baixa)")
        
        if current_price > ma_fast:
            buy_score += 1
            reasons.append("Preço acima da MA rápida")
        else:
            sell_score += 1
            reasons.append("Preço abaixo da MA rápida")
        
        # MACD Analysis
        macd = indicators.get('macd', 0)
        macd_signal = indicators.get('macd_signal', 0)
        macd_diff = indicators.get('macd_diff', 0)
        
        if macd > macd_signal and macd_diff > 0:
            buy_score += 2
            reasons.append("MACD positivo e acima do sinal")
        elif macd < macd_signal and macd_diff < 0:
            sell_score += 2
            reasons.append("MACD negativo e abaixo do sinal")
        
        # Price Momentum
        price_change = indicators.get('price_change', 0)
        if price_change > 0.1:
            buy_score += 1
            reasons.append("Momentum positivo")
        elif price_change < -0.1:
            sell_score += 1
            reasons.append("Momentum negativo")
        
        # Determinar ação e confiança
        total_score = buy_score + sell_score
        if total_score == 0:
            action = Action.HOLD
            confidence = 0.0
            reason = "Indicadores neutros"
        elif buy_score > sell_score:
            action = Action.BUY
            confidence = min(0.95, buy_score / max(total_score, 1) * 1.2)
            reason = f"BUY: {', '.join(reasons[:3])}"
        elif sell_score > buy_score:
            action = Action.SELL
            confidence = min(0.95, sell_score / max(total_score, 1) * 1.2)
            reason = f"SELL: {', '.join(reasons[:3])}"
        else:
            action = Action.HOLD
            confidence = 0.5
            reason = "Sinais balanceados"
        
        return action, confidence, reason

