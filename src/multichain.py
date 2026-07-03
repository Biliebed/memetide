#!/usr/bin/env python3
"""
Multi-chain DexScreener Integration

Supports: Ethereum, Solana, Base, Arbitrum, Polygon
"""

import httpx
from typing import Optional, Dict, Any, List
from enum import Enum


class Chain(str, Enum):
    """Supported blockchain networks"""
    ETHEREUM = "ethereum"
    SOLANA = "solana"
    BASE = "base"
    ARBITRUM = "arbitrum"
    POLYGON = "polygon"
    BSC = "bsc"  # Binance Smart Chain


class MultiChainDexScreener:
    """Fetch token metrics from multiple chains"""
    
    def __init__(self):
        self.base_url = "https://api.dexscreener.com/latest/dex"
        self.timeout = 5.0
    
    async def search_token_multi_chain(
        self,
        token_symbol: str,
        chains: Optional[List[Chain]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search token across multiple chains
        
        Args:
            token_symbol: Token symbol (e.g., "PEPE", "BONK")
            chains: List of chains to search (default: all)
        
        Returns:
            List of results from all chains
        """
        if chains is None:
            chains = [Chain.ETHEREUM, Chain.SOLANA, Chain.BASE]
        
        results = []
        
        for chain in chains:
            try:
                result = await self.search_token(token_symbol, chain)
                if result:
                    result["chain"] = chain.value
                    results.append(result)
            except Exception as e:
                print(f"⚠️  {chain.value} search failed for ${token_symbol}: {e}")
        
        # Sort by market cap (highest first)
        results.sort(
            key=lambda x: x.get("market_cap", 0) or 0,
            reverse=True
        )
        
        return results
    
    async def search_token(
        self,
        token_symbol: str,
        chain: Chain = Chain.ETHEREUM
    ) -> Optional[Dict[str, Any]]:
        """
        Search for token on specific chain
        
        Args:
            token_symbol: Token symbol
            chain: Blockchain to search
        
        Returns:
            Token metrics dict or None
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # DexScreener search endpoint
                response = await client.get(
                    f"{self.base_url}/search",
                    params={"q": token_symbol}
                )
                
                if response.status_code != 200:
                    return None
                
                data = response.json()
                pairs = data.get("pairs", [])
                
                if not pairs:
                    return None
                
                # Filter by chain
                chain_pairs = [
                    p for p in pairs
                    if p.get("chainId", "").lower() == chain.value.lower()
                ]
                
                if not chain_pairs:
                    return None
                
                # Get highest liquidity pair
                pair = max(
                    chain_pairs,
                    key=lambda x: float(x.get("liquidity", {}).get("usd", 0) or 0)
                )
                
                return self._extract_metrics(pair, chain)
        
        except Exception as e:
            print(f"DexScreener {chain.value} error for ${token_symbol}: {e}")
            return None
    
    def _extract_metrics(
        self,
        pair: Dict[str, Any],
        chain: Chain
    ) -> Dict[str, Any]:
        """Extract standardized metrics from pair data"""
        # Handle different address formats
        if chain == Chain.SOLANA:
            contract = pair.get("baseToken", {}).get("address", "")
        else:
            contract = pair.get("baseToken", {}).get("address", "")
        
        price = float(pair.get("priceUsd", 0) or 0)
        liquidity_data = pair.get("liquidity", {})
        liquidity = float(liquidity_data.get("usd", 0) or 0)
        
        # Market cap calculation
        fdv = float(pair.get("fdv", 0) or 0)
        market_cap = fdv if fdv > 0 else None
        
        # Token age
        created_at = pair.get("pairCreatedAt")
        age_hours = None
        if created_at:
            import time
            age_seconds = time.time() - (created_at / 1000)  # Convert ms to s
            age_hours = age_seconds / 3600
        
        # Volume
        volume_24h = float(pair.get("volume", {}).get("h24", 0) or 0)
        
        # Price change
        price_change_24h = float(pair.get("priceChange", {}).get("h24", 0) or 0)
        
        return {
            "contract_address": contract,
            "chain": chain.value,
            "price_usd": price,
            "market_cap": market_cap,
            "liquidity": liquidity,
            "volume_24h": volume_24h,
            "price_change_24h": price_change_24h,
            "age_hours": age_hours,
            "dex": pair.get("dexId", "unknown"),
            "pair_address": pair.get("pairAddress", "")
        }
    
    async def get_trending_pairs(
        self,
        chain: Chain = Chain.ETHEREUM,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get trending pairs on a chain
        
        Args:
            chain: Blockchain
            limit: Max results
        
        Returns:
            List of trending pairs
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # This endpoint may vary - check DexScreener docs
                response = await client.get(
                    f"{self.base_url}/tokens/trending/{chain.value}"
                )
                
                if response.status_code != 200:
                    return []
                
                data = response.json()
                pairs = data.get("pairs", [])[:limit]
                
                return [self._extract_metrics(p, chain) for p in pairs]
        
        except Exception as e:
            print(f"Failed to get trending pairs for {chain.value}: {e}")
            return []


# Chain-specific helpers

def get_chain_explorer_url(chain: Chain, address: str) -> str:
    """Get block explorer URL for token"""
    explorers = {
        Chain.ETHEREUM: f"https://etherscan.io/token/{address}",
        Chain.SOLANA: f"https://solscan.io/token/{address}",
        Chain.BASE: f"https://basescan.org/token/{address}",
        Chain.ARBITRUM: f"https://arbiscan.io/token/{address}",
        Chain.POLYGON: f"https://polygonscan.com/token/{address}",
        Chain.BSC: f"https://bscscan.com/token/{address}"
    }
    return explorers.get(chain, "")


def get_chain_icon(chain: Chain) -> str:
    """Get emoji icon for chain"""
    icons = {
        Chain.ETHEREUM: "Ξ",
        Chain.SOLANA: "◎",
        Chain.BASE: "🔵",
        Chain.ARBITRUM: "🔷",
        Chain.POLYGON: "🟣",
        Chain.BSC: "🟡"
    }
    return icons.get(chain, "⛓️")
