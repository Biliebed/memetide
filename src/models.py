from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List
from enum import Enum


class RiskLevel(str, Enum):
    """Risk assessment levels"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ConfidenceLevel(str, Enum):
    """Confidence in trend prediction"""
    HIGH = "high"      # 🔥
    MEDIUM = "medium"  # ⚠️
    LOW = "low"        # ❌


@dataclass
class TokenMention:
    """Single token mention data"""
    token_symbol: str
    timestamp: str
    text: str
    author: Optional[str] = None
    likes: int = 0
    retweets: int = 0
    
    def to_dict(self):
        return asdict(self)


@dataclass
class SentimentScore:
    """Sentiment analysis result"""
    positive: float  # 0.0 - 1.0
    negative: float
    neutral: float
    compound: float  # Overall score -1.0 to 1.0
    
    @property
    def is_positive(self) -> bool:
        return self.compound > 0.1
    
    @property
    def is_negative(self) -> bool:
        return self.compound < -0.1
    
    @property
    def percentage_positive(self) -> float:
        return round(self.positive * 100, 1)
    
    def to_dict(self):
        return asdict(self)


@dataclass
class TokenMetrics:
    """Token on-chain metrics"""
    contract_address: Optional[str]
    price_usd: Optional[float]
    market_cap: Optional[float]
    liquidity: Optional[float]
    holder_count: Optional[int]
    age_hours: Optional[float]
    
    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class TrendPrediction:
    """Main prediction result"""
    token_symbol: str
    mention_count: int
    mentions_per_hour: float
    sentiment: SentimentScore
    risk_level: RiskLevel
    confidence: ConfidenceLevel
    score: float  # 0-100
    metrics: Optional[TokenMetrics]
    first_seen: str
    last_updated: str
    sample_tweets: List[str]
    
    def to_dict(self):
        return {
            "token_symbol": self.token_symbol,
            "mention_count": self.mention_count,
            "mentions_per_hour": round(self.mentions_per_hour, 2),
            "sentiment": self.sentiment.to_dict(),
            "risk_level": self.risk_level.value,
            "confidence": self.confidence.value,
            "score": round(self.score, 1),
            "metrics": self.metrics.to_dict() if self.metrics else None,
            "first_seen": self.first_seen,
            "last_updated": self.last_updated,
            "sample_tweets": self.sample_tweets[:3]  # Top 3
        }
    
    def to_emoji(self) -> str:
        """Get confidence emoji"""
        return {
            ConfidenceLevel.HIGH: "🔥",
            ConfidenceLevel.MEDIUM: "⚠️",
            ConfidenceLevel.LOW: "❌"
        }[self.confidence]


@dataclass
class ScanResult:
    """Complete scan result"""
    scan_id: str
    timestamp: str
    total_mentions: int
    unique_tokens: int
    predictions: List[TrendPrediction]
    duration_seconds: float
    
    def to_dict(self):
        return {
            "scan_id": self.scan_id,
            "timestamp": self.timestamp,
            "total_mentions": self.total_mentions,
            "unique_tokens": self.unique_tokens,
            "predictions": [p.to_dict() for p in self.predictions],
            "duration_seconds": round(self.duration_seconds, 2)
        }
    
    def get_high_confidence(self) -> List[TrendPrediction]:
        """Get only high confidence predictions"""
        return [p for p in self.predictions if p.confidence == ConfidenceLevel.HIGH]
