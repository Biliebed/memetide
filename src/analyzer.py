import re
from typing import List, Dict
from collections import defaultdict
from datetime import datetime, timedelta
from textblob import TextBlob
from .models import TokenMention, SentimentScore


class SentimentAnalyzer:
    """Analyze sentiment of crypto tweets"""
    
    def __init__(self):
        # Crypto-specific sentiment keywords
        self.positive_keywords = [
            "moon", "bullish", "gem", "alpha", "breakout",
            "pump", "rocket", "lfg", "wagmi", "gm", "based",
            "gigabrain", "send it", "100x", "1000x"
        ]
        
        self.negative_keywords = [
            "scam", "rug", "dump", "bearish", "ngmi",
            "rekt", "dead", "exit", "avoid", "warning",
            "honeypot", "suspicious"
        ]
        
        self.hype_keywords = [
            "fomo", "early", "don't miss", "last chance",
            "fair launch", "stealth launch", "presale"
        ]
    
    def analyze(self, text: str) -> SentimentScore:
        """
        Analyze sentiment with crypto context
        """
        # Clean text
        text_lower = text.lower()
        
        # TextBlob baseline sentiment
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 to 1
        
        # Crypto keyword boost
        positive_count = sum(1 for word in self.positive_keywords if word in text_lower)
        negative_count = sum(1 for word in self.negative_keywords if word in text_lower)
        hype_count = sum(1 for word in self.hype_keywords if word in text_lower)
        
        # Adjust sentiment based on crypto keywords (bigger boost for crypto slang)
        crypto_boost = (positive_count - negative_count) * 0.25
        hype_boost = hype_count * 0.15
        
        adjusted_polarity = polarity + crypto_boost + hype_boost
        adjusted_polarity = max(-1.0, min(1.0, adjusted_polarity))  # Clamp
        
        # Convert to positive/negative/neutral scores
        if adjusted_polarity > 0:
            positive = adjusted_polarity
            negative = 0.0
            neutral = 1.0 - positive
        elif adjusted_polarity < 0:
            negative = abs(adjusted_polarity)
            positive = 0.0
            neutral = 1.0 - negative
        else:
            positive = 0.0
            negative = 0.0
            neutral = 1.0
        
        return SentimentScore(
            positive=positive,
            negative=negative,
            neutral=neutral,
            compound=adjusted_polarity
        )
    
    def aggregate_sentiment(self, mentions: List[TokenMention]) -> SentimentScore:
        """
        Aggregate sentiment from multiple mentions
        """
        if not mentions:
            return SentimentScore(0.0, 0.0, 1.0, 0.0)
        
        sentiments = [self.analyze(m.text) for m in mentions]
        
        # Weighted average (weight by engagement)
        total_weight = 0
        weighted_compound = 0.0
        
        for mention, sentiment in zip(mentions, sentiments):
            weight = 1 + (mention.likes * 0.1) + (mention.retweets * 0.2)
            weighted_compound += sentiment.compound * weight
            total_weight += weight
        
        avg_compound = weighted_compound / total_weight if total_weight > 0 else 0.0
        
        # Convert compound to scores
        if avg_compound > 0:
            positive = avg_compound
            negative = 0.0
            neutral = 1.0 - positive
        elif avg_compound < 0:
            negative = abs(avg_compound)
            positive = 0.0
            neutral = 1.0 - negative
        else:
            positive = 0.0
            negative = 0.0
            neutral = 1.0
        
        return SentimentScore(
            positive=positive,
            negative=negative,
            neutral=neutral,
            compound=avg_compound
        )


class TokenExtractor:
    """Extract token symbols from text"""
    
    # Patterns for token detection
    PATTERNS = [
        r'\$([A-Z][A-Z0-9]{2,10})\b',  # $TOKEN format
        r'\b([A-Z][A-Z0-9]{2,10})\s+(?:coin|token)\b',  # TOKEN coin/token
        r'#([A-Za-z][A-Za-z0-9]{2,10})',  # #token hashtag
    ]
    
    # Known tokens to filter out (too generic)
    BLACKLIST = {
        "BTC", "ETH", "BNB", "SOL", "ADA", "XRP", "DOGE",
        "USDT", "USDC", "DAI", "THE", "FOR", "AND", "NOT",
        "USD", "EUR", "GBP", "ALL", "NEW", "TOP", "GET"
    }
    
    def extract_tokens(self, text: str) -> List[str]:
        """
        Extract token symbols from text
        """
        tokens = set()
        
        for pattern in self.PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            tokens.update(m.upper() for m in matches)
        
        # Filter blacklist
        tokens = {t for t in tokens if t not in self.BLACKLIST}
        
        # Filter length (2-10 chars)
        tokens = {t for t in tokens if 2 <= len(t) <= 10}
        
        return list(tokens)
    
    def extract_from_mentions(self, mentions: List[TokenMention]) -> Dict[str, List[TokenMention]]:
        """
        Group mentions by token symbol
        """
        token_map = defaultdict(list)
        
        for mention in mentions:
            tokens = self.extract_tokens(mention.text)
            for token in tokens:
                token_map[token].append(mention)
        
        return dict(token_map)


def calculate_velocity(mentions: List[TokenMention], hours: float = 1.0) -> float:
    """
    Calculate mentions per hour
    """
    if not mentions:
        return 0.0
    
    # Parse timestamps
    timestamps = []
    for m in mentions:
        try:
            ts = datetime.fromisoformat(m.timestamp.replace('Z', '+00:00'))
            timestamps.append(ts)
        except:
            continue
    
    if len(timestamps) < 2:
        return len(mentions) / hours
    
    # Calculate time span
    time_span = (max(timestamps) - min(timestamps)).total_seconds() / 3600
    
    if time_span < 0.1:  # Less than 6 minutes
        time_span = hours
    
    return len(mentions) / time_span
