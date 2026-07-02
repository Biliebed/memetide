"""
MemeTide - Memecoin Trend Predictor
"""

__version__ = "1.0.0"
__author__ = "MemeTide Team"

from .models import (
    TrendPrediction,
    ScanResult,
    RiskLevel,
    ConfidenceLevel,
    SentimentScore,
    TokenMetrics
)

from .engine import MemeTideEngine

__all__ = [
    'MemeTideEngine',
    'TrendPrediction',
    'ScanResult',
    'RiskLevel',
    'ConfidenceLevel',
    'SentimentScore',
    'TokenMetrics'
]
