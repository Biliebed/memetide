from typing import List, Optional
from .models import (
    TokenMention, SentimentScore, TrendPrediction,
    RiskLevel, ConfidenceLevel, TokenMetrics
)


class RiskScorer:
    """
    Calculate risk level for tokens
    """
    
    def __init__(self):
        # Risk indicators (keywords that suggest scam/risk)
        self.scam_keywords = [
            "scam", "rug", "honeypot", "sus", "suspicious",
            "avoid", "warning", "exit", "dump", "rugpull"
        ]
        
        self.hype_keywords = [
            "100x", "1000x", "moon", "rocket", "fomo",
            "don't miss", "last chance", "presale", "stealth"
        ]
    
    def calculate_risk(
        self,
        mentions: List[TokenMention],
        sentiment: SentimentScore,
        metrics: Optional[TokenMetrics] = None
    ) -> RiskLevel:
        """
        Calculate overall risk level
        """
        risk_score = 0.0  # 0 = low risk, 100 = very high risk
        
        # 1. Negative sentiment risk
        if sentiment.is_negative:
            risk_score += 30
        
        # 2. Scam keyword detection
        scam_mentions = sum(
            1 for m in mentions
            if any(keyword in m.text.lower() for keyword in self.scam_keywords)
        )
        scam_ratio = scam_mentions / len(mentions) if mentions else 0
        risk_score += scam_ratio * 40
        
        # 3. Excessive hype risk (pump & dump indicator)
        hype_mentions = sum(
            1 for m in mentions
            if any(keyword in m.text.lower() for keyword in self.hype_keywords)
        )
        hype_ratio = hype_mentions / len(mentions) if mentions else 0
        if hype_ratio > 0.5:  # More than 50% are hype
            risk_score += 20
        
        # 4. Low engagement risk (bot activity)
        if mentions:
            avg_engagement = sum(m.likes + m.retweets for m in mentions) / len(mentions)
            if avg_engagement < 10:  # Very low engagement
                risk_score += 15
        
        # 5. On-chain metrics risk (if available)
        if metrics:
            # New token = higher risk
            if metrics.age_hours and metrics.age_hours < 24:
                risk_score += 15
            
            # Low liquidity = high risk
            if metrics.liquidity and metrics.liquidity < 10000:
                risk_score += 20
            
            # Few holders = high risk
            if metrics.holder_count and metrics.holder_count < 50:
                risk_score += 15
        
        # Map score to risk level
        if risk_score < 20:
            return RiskLevel.VERY_LOW
        elif risk_score < 40:
            return RiskLevel.LOW
        elif risk_score < 60:
            return RiskLevel.MEDIUM
        elif risk_score < 80:
            return RiskLevel.HIGH
        else:
            return RiskLevel.VERY_HIGH
    
    def calculate_confidence(
        self,
        mention_count: int,
        mentions_per_hour: float,
        sentiment: SentimentScore,
        risk: RiskLevel
    ) -> tuple[ConfidenceLevel, float]:
        """
        Calculate confidence in prediction
        Returns (confidence_level, score_0_100)
        """
        score = 0.0
        
        # 1. Volume factor (0-30 points)
        if mentions_per_hour > 100:
            score += 30
        elif mentions_per_hour > 50:
            score += 25
        elif mentions_per_hour > 20:
            score += 20
        elif mentions_per_hour > 5:
            score += 15
        elif mention_count >= 5:
            score += 12  # Lower threshold - 5+ mentions is decent
        else:
            score += mention_count * 2  # Boost for small counts
        
        # 2. Sentiment factor (0-30 points)
        if sentiment.is_positive:
            score += sentiment.percentage_positive * 0.3
        
        # 3. Consistency factor (0-20 points)
        # High mentions + positive sentiment = consistent signal
        if mention_count >= 5 and sentiment.percentage_positive > 65:
            score += 20
        elif mention_count >= 3 and sentiment.percentage_positive > 50:
            score += 15
        elif mention_count >= 3:
            score += 5
        
        # 4. Risk penalty (-40 to 0 points)
        risk_penalty = {
            RiskLevel.VERY_LOW: 0,
            RiskLevel.LOW: -5,
            RiskLevel.MEDIUM: -10,
            RiskLevel.HIGH: -25,
            RiskLevel.VERY_HIGH: -40
        }
        score += risk_penalty[risk]
        
        # Clamp to 0-100
        score = max(0, min(100, score))
        
        # Determine confidence level
        if score >= 70:
            confidence = ConfidenceLevel.HIGH
        elif score >= 40:
            confidence = ConfidenceLevel.MEDIUM
        else:
            confidence = ConfidenceLevel.LOW
        
        return confidence, score
