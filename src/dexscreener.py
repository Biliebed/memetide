"""
DexScreener Integration

Fetch on-chain metrics for memecoins:
- Price (USD)
- Market cap
- Liquidity
- Volume (24h)
- Price changes
- Holder count (from chain data)
"""

import httpx
import asyncio
from typing import Optional, Dict, List
from datetime import datetime, timedelta

try:
    from .models import TokenMetrics
except ImportError:
    from models import TokenMetrics


class DexScreenerClient:
    """
    DexScreener API client for on-chain token data
    
    API Docs: https://docs.dexscreener.com/api/reference
    Rate Limit: 300 requests/minute
    """
    
    BASE_URL = "https://api.dexscreener.com/latest/dex"
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self._cache: Dict[str, tuple] = {}  # symbol -> (data, timestamp)
        self.cache_ttl = 60  # seconds
    
    async def search_token(self, symbol: str) -> Optional[Dict]:
        """
        Search for token by symbol
        
        Args:
            symbol: Token symbol (e.g., "PEPE", "FLOKI")
        
        Returns:
            Best matching pair data or None
        """
        # Check cache
        if symbol in self._cache:
            data, timestamp = self._cache[symbol]
            if datetime.now().timestamp() - timestamp < self.cache_ttl:
                return data
        
        try:
            # Clean symbol
            clean_symbol = symbol.replace("$", "").strip().upper()
            
            # Search API
            url = f"{self.BASE_URL}/search?q={clean_symbol}"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
            
            # Get best pair (highest liquidity)
            pairs = data.get("pairs", [])
            if not pairs:
                return None
            
            # Filter and sort
            valid_pairs = [
                p for p in pairs
                if p.get("baseToken", {}).get("symbol", "").upper() == clean_symbol
                and p.get("liquidity", {}).get("usd", 0) > 1000  # Min $1k liquidity
            ]
            
            if not valid_pairs:
                # Fallback: just take first pair
                best_pair = pairs[0]
            else:
                # Sort by liquidity
                best_pair = max(valid_pairs, key=lambda p: p.get("liquidity", {}).get("usd", 0))
            
            # Cache result
            self._cache[symbol] = (best_pair, datetime.now().timestamp())
            
            return best_pair
        
        except Exception as e:
            print(f"[DexScreener] Error fetching {symbol}: {e}")
            return None
    
    async def get_metrics(self, symbol: str) -> Optional[TokenMetrics]:
        """
        Get token metrics from DexScreener
        
        Args:
            symbol: Token symbol
        
        Returns:
            TokenMetrics or None if not found
        """
        pair_data = await self.search_token(symbol)
        
        if not pair_data:
            return None
        
        try:
            # Extract metrics
            base_token = pair_data.get("baseToken", {})
            liquidity = pair_data.get("liquidity", {})
            fdv = pair_data.get("fdv")  # Fully Diluted Valuation
            
            # Calculate token age
            pair_created = pair_data.get("pairCreatedAt")
            age_hours = None
            if pair_created:
                created_dt = datetime.fromtimestamp(pair_created / 1000)
                age_hours = (datetime.now() - created_dt).total_seconds() / 3600
            
            # Parse price
            price_usd = pair_data.get("priceUsd")
            if price_usd:
                price_usd = float(price_usd)
            
            # Parse liquidity
            liquidity_usd = liquidity.get("usd")
            if liquidity_usd:
                liquidity_usd = float(liquidity_usd)
            
            # Parse market cap (use FDV as proxy)
            market_cap = None
            if fdv:
                market_cap = float(fdv)
            
            return TokenMetrics(
                contract_address=base_token.get("address"),
                price_usd=price_usd,
                market_cap=market_cap,
                liquidity=liquidity_usd,
                holder_count=None,  # Not available in DexScreener
                age_hours=age_hours
            )
        
        except Exception as e:
            print(f"[DexScreener] Error parsing metrics for {symbol}: {e}")
            return None
    
    async def get_batch_metrics(self, symbols: List[str]) -> Dict[str, Optional[TokenMetrics]]:
        """
        Fetch metrics for multiple tokens in parallel
        
        Args:
            symbols: List of token symbols
        
        Returns:
            Dict mapping symbol -> TokenMetrics
        """
        tasks = [self.get_metrics(symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        metrics = {}
        for symbol, result in zip(symbols, results):
            if isinstance(result, Exception):
                print(f"[DexScreener] Error for {symbol}: {result}")
                metrics[symbol] = None
            else:
                metrics[symbol] = result
        
        return metrics
    
    def get_pair_url(self, symbol: str) -> Optional[str]:
        """Get DexScreener URL for a token (from cache)"""
        if symbol in self._cache:
            data, _ = self._cache[symbol]
            return data.get("url")
        return None


# --- Helper Functions ---

async def enrich_predictions_with_metrics(predictions: List, client: DexScreenerClient = None):
    """
    Enrich predictions with on-chain metrics
    
    Args:
        predictions: List of TrendPrediction objects
        client: DexScreenerClient instance (creates new if None)
    
    Returns:
        Updated predictions list
    """
    if not predictions:
        return predictions
    
    if client is None:
        client = DexScreenerClient()
    
    # Extract symbols
    symbols = [p.token_symbol for p in predictions]
    
    # Fetch metrics in parallel
    print(f"[DexScreener] Fetching on-chain data for {len(symbols)} tokens...")
    metrics_map = await client.get_batch_metrics(symbols)
    
    # Attach metrics
    for prediction in predictions:
        metrics = metrics_map.get(prediction.token_symbol)
        prediction.metrics = metrics
        
        if metrics:
            print(f"  ✅ {prediction.token_symbol}: ${metrics.price_usd:.8f}, "
                  f"Liq: ${metrics.liquidity:,.0f}" if metrics.liquidity else "")
        else:
            print(f"  ⚠️ {prediction.token_symbol}: No on-chain data found")
    
    return predictions


# --- Usage Example ---

async def main():
    """Test DexScreener client"""
    client = DexScreenerClient()
    
    print("\n" + "="*60)
    print("DEXSCREENER CLIENT TEST")
    print("="*60 + "\n")
    
    # Test single token
    print("[1] Testing single token: PEPE")
    metrics = await client.get_metrics("PEPE")
    
    if metrics:
        print(f"✅ Found PEPE:")
        print(f"   Price: ${metrics.price_usd:.8f}")
        print(f"   Market Cap: ${metrics.market_cap:,.0f}" if metrics.market_cap else "   Market Cap: N/A")
        print(f"   Liquidity: ${metrics.liquidity:,.0f}" if metrics.liquidity else "   Liquidity: N/A")
        print(f"   Age: {metrics.age_hours:.1f} hours" if metrics.age_hours else "   Age: N/A")
        print(f"   Contract: {metrics.contract_address}")
        print(f"   URL: {client.get_pair_url('PEPE')}")
    else:
        print("❌ PEPE not found")
    
    # Test batch
    print("\n[2] Testing batch: PEPE, FLOKI, DOGE")
    batch = await client.get_batch_metrics(["PEPE", "FLOKI", "DOGE"])
    
    for symbol, metrics in batch.items():
        if metrics:
            print(f"✅ {symbol}: ${metrics.price_usd:.8f}, Liq: ${metrics.liquidity:,.0f}")
        else:
            print(f"❌ {symbol}: Not found")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
