import uuid
import time
from datetime import datetime
from typing import List
from .models import TrendPrediction, ScanResult, TokenMetrics
from .scraper import TwitterScraper, MockTwitterScraper
from .analyzer import SentimentAnalyzer, TokenExtractor, calculate_velocity
from .risk import RiskScorer
from .dexscreener import DexScreenerClient


class MemeTideEngine:
    """
    Main MemeTide prediction engine
    """
    
    def __init__(self, use_mock_data: bool = True, fetch_onchain: bool = True):
        """
        Args:
            use_mock_data: If True, use mock Twitter data for testing
            fetch_onchain: If True, fetch on-chain metrics from DexScreener
        """
        if use_mock_data:
            self.scraper = MockTwitterScraper()
            print("[Engine] Using MOCK Twitter data (for testing)")
        else:
            self.scraper = TwitterScraper()
            print("[Engine] Using REAL Twitter scraping")
        
        self.sentiment_analyzer = SentimentAnalyzer()
        self.token_extractor = TokenExtractor()
        self.risk_scorer = RiskScorer()
        
        # On-chain data fetcher
        self.fetch_onchain = fetch_onchain
        if fetch_onchain:
            self.dex_client = DexScreenerClient()
            print("[Engine] On-chain metrics ENABLED (DexScreener)")
        else:
            self.dex_client = None
            print("[Engine] On-chain metrics DISABLED")
    
    async def scan(self, min_mentions: int = 3) -> ScanResult:
        """
        Run full memecoin trend scan
        
        Args:
            min_mentions: Minimum mentions required to consider a token
        
        Returns:
            ScanResult with predictions
        """
        start_time = time.time()
        scan_id = str(uuid.uuid4())[:8]
        
        print(f"\n{'='*60}")
        print(f"MEMETIDE SCAN #{scan_id}")
        print(f"{'='*60}\n")
        
        # Step 1: Scrape Twitter
        print("[1/4] Scraping Twitter...")
        mentions = await self.scraper.scan_all()
        
        if not mentions:
            print("⚠️  No mentions found")
            return ScanResult(
                scan_id=scan_id,
                timestamp=datetime.utcnow().isoformat(),
                total_mentions=0,
                unique_tokens=0,
                predictions=[],
                duration_seconds=time.time() - start_time
            )
        
        # Step 2: Extract tokens
        print(f"\n[2/4] Extracting tokens from {len(mentions)} mentions...")
        token_mentions = self.token_extractor.extract_from_mentions(mentions)
        
        # Filter by minimum mentions
        token_mentions = {
            token: ms for token, ms in token_mentions.items()
            if len(ms) >= min_mentions
        }
        
        print(f"Found {len(token_mentions)} tokens with >= {min_mentions} mentions")
        
        if not token_mentions:
            print("⚠️  No tokens met minimum threshold")
            return ScanResult(
                scan_id=scan_id,
                timestamp=datetime.utcnow().isoformat(),
                total_mentions=len(mentions),
                unique_tokens=0,
                predictions=[],
                duration_seconds=time.time() - start_time
            )
        
        # Step 3: Analyze each token
        print(f"\n[3/4] Analyzing {len(token_mentions)} tokens...")
        predictions = []
        
        for token_symbol, token_ms in token_mentions.items():
            try:
                # Sentiment analysis
                sentiment = self.sentiment_analyzer.aggregate_sentiment(token_ms)
                
                # Velocity calculation
                velocity = calculate_velocity(token_ms, hours=1.0)
                
                # Fetch on-chain metrics (if enabled)
                metrics = None
                if self.fetch_onchain and self.dex_client:
                    metrics = await self.dex_client.get_metrics(token_symbol)
                
                # Risk assessment
                risk = self.risk_scorer.calculate_risk(
                    token_ms,
                    sentiment,
                    metrics=metrics  # Now includes on-chain data
                )
                
                # Confidence calculation
                confidence, score = self.risk_scorer.calculate_confidence(
                    mention_count=len(token_ms),
                    mentions_per_hour=velocity,
                    sentiment=sentiment,
                    risk=risk
                )
                
                # Sample tweets
                sample_tweets = [
                    m.text[:100] + "..." if len(m.text) > 100 else m.text
                    for m in sorted(token_ms, key=lambda x: x.likes + x.retweets, reverse=True)[:3]
                ]
                
                # Create prediction
                prediction = TrendPrediction(
                    token_symbol=token_symbol,
                    mention_count=len(token_ms),
                    mentions_per_hour=velocity,
                    sentiment=sentiment,
                    risk_level=risk,
                    confidence=confidence,
                    score=score,
                    metrics=metrics,  # On-chain data attached
                    first_seen=min(m.timestamp for m in token_ms),
                    last_updated=datetime.utcnow().isoformat(),
                    sample_tweets=sample_tweets
                )
                
                predictions.append(prediction)
                
                # Log
                emoji = prediction.to_emoji()
                metrics_str = ""
                if metrics:
                    metrics_str = f", ${metrics.price_usd:.8f}" if metrics.price_usd else ""
                    if metrics.liquidity:
                        metrics_str += f", Liq: ${metrics.liquidity:,.0f}"
                
                print(f"  {emoji} {token_symbol}: "
                      f"{len(token_ms)} mentions, "
                      f"{sentiment.percentage_positive}% positive, "
                      f"{risk.value} risk"
                      f"{metrics_str}")
            
            except Exception as e:
                print(f"  ❌ Error analyzing {token_symbol}: {e}")
                continue
        
        # Step 4: Sort predictions by score
        print(f"\n[4/4] Ranking predictions...")
        predictions.sort(key=lambda p: p.score, reverse=True)
        
        # Create result
        result = ScanResult(
            scan_id=scan_id,
            timestamp=datetime.utcnow().isoformat(),
            total_mentions=len(mentions),
            unique_tokens=len(predictions),
            predictions=predictions,
            duration_seconds=time.time() - start_time
        )
        
        print(f"\n{'='*60}")
        print(f"SCAN COMPLETE")
        print(f"{'='*60}")
        print(f"Duration: {result.duration_seconds:.2f}s")
        print(f"Total mentions: {result.total_mentions}")
        print(f"Unique tokens: {result.unique_tokens}")
        print(f"High confidence: {len(result.get_high_confidence())}")
        print(f"{'='*60}\n")
        
        return result
    
    def format_results(self, result: ScanResult, top_n: int = 10) -> str:
        """
        Format scan results as human-readable text
        """
        output = []
        output.append(f"\n🌊 MEMETIDE SCAN RESULTS")
        output.append(f"Scan ID: {result.scan_id}")
        output.append(f"Time: {result.timestamp}")
        output.append(f"Duration: {result.duration_seconds:.2f}s\n")
        
        if not result.predictions:
            output.append("No trending tokens found.\n")
            return "\n".join(output)
        
        output.append(f"📊 TOP {min(top_n, len(result.predictions))} PREDICTIONS:\n")
        
        for i, pred in enumerate(result.predictions[:top_n], 1):
            emoji = pred.to_emoji()
            output.append(f"{i}. {emoji} ${pred.token_symbol}")
            output.append(f"   Score: {pred.score:.1f}/100")
            output.append(f"   Mentions: {pred.mention_count} ({pred.mentions_per_hour:.1f}/hr)")
            output.append(f"   Sentiment: {pred.sentiment.percentage_positive:.1f}% positive")
            output.append(f"   Risk: {pred.risk_level.value.upper()}")
            output.append(f"   Confidence: {pred.confidence.value.upper()}")
            
            # On-chain metrics (if available)
            if pred.metrics:
                m = pred.metrics
                output.append(f"   📊 On-Chain:")
                if m.price_usd:
                    output.append(f"      Price: ${m.price_usd:.8f}")
                if m.market_cap:
                    output.append(f"      Market Cap: ${m.market_cap:,.0f}")
                if m.liquidity:
                    output.append(f"      Liquidity: ${m.liquidity:,.0f}")
                if m.age_hours:
                    days = int(m.age_hours / 24)
                    hours = int(m.age_hours % 24)
                    output.append(f"      Age: {days}d {hours}h")
            
            output.append("")  # Empty line between tokens
        
        return "\n".join(output)
