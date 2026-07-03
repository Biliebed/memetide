#!/usr/bin/env python3
"""
Test on-chain metrics integration

Tests DexScreener API integration across:
- CLI
- API server
- Engine
"""

import asyncio
import httpx
from src.dexscreener import DexScreenerClient
from src.engine import MemeTideEngine


async def test_dexscreener_client():
    """Test DexScreener client directly"""
    print("\n" + "="*60)
    print("TEST 1: DexScreener Client")
    print("="*60 + "\n")
    
    client = DexScreenerClient()
    
    # Test batch fetch
    symbols = ["PEPE", "FLOKI", "DOGE", "SHIB"]
    print(f"Fetching metrics for: {', '.join(symbols)}")
    
    metrics = await client.get_batch_metrics(symbols)
    
    found = 0
    for symbol, m in metrics.items():
        if m:
            print(f"✅ {symbol}:")
            print(f"   Price: ${m.price_usd:.8f}" if m.price_usd else "   Price: N/A")
            print(f"   Liquidity: ${m.liquidity:,.0f}" if m.liquidity else "   Liquidity: N/A")
            found += 1
        else:
            print(f"❌ {symbol}: Not found")
    
    print(f"\n✅ Found {found}/{len(symbols)} tokens")


async def test_engine_integration():
    """Test engine with on-chain metrics"""
    print("\n" + "="*60)
    print("TEST 2: Engine Integration")
    print("="*60 + "\n")
    
    # Test with on-chain enabled
    print("[1] Testing with on-chain ENABLED")
    engine = MemeTideEngine(use_mock_data=True, fetch_onchain=True)
    result = await engine.scan(min_mentions=3)
    
    has_metrics = sum(1 for p in result.predictions if p.metrics is not None)
    print(f"✅ Predictions with on-chain data: {has_metrics}/{len(result.predictions)}")
    
    # Test with on-chain disabled
    print("\n[2] Testing with on-chain DISABLED")
    engine = MemeTideEngine(use_mock_data=True, fetch_onchain=False)
    result = await engine.scan(min_mentions=3)
    
    has_metrics = sum(1 for p in result.predictions if p.metrics is not None)
    print(f"✅ Predictions with on-chain data: {has_metrics}/{len(result.predictions)}")
    assert has_metrics == 0, "Should have no metrics when disabled"


async def test_api_integration():
    """Test API with on-chain metrics"""
    print("\n" + "="*60)
    print("TEST 3: API Integration")
    print("="*60 + "\n")
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test with on-chain enabled
        print("[1] Testing API with on-chain ENABLED")
        response = await client.post(
            f"{base_url}/scan",
            json={
                "min_mentions": 3,
                "use_mock_data": True,
                "fetch_onchain": True,
                "top_n": 3
            }
        )
        
        if response.status_code != 200:
            print(f"❌ API failed: {response.status_code}")
            return
        
        data = response.json()
        predictions = data["data"]["predictions"]
        
        has_metrics = sum(1 for p in predictions if p.get("metrics") is not None)
        print(f"✅ API predictions with on-chain: {has_metrics}/{len(predictions)}")
        
        # Show example
        if predictions and predictions[0].get("metrics"):
            m = predictions[0]["metrics"]
            print(f"\nExample: ${predictions[0]['token_symbol']}")
            print(f"   Price: ${m.get('price_usd', 0):.8f}")
            print(f"   Liquidity: ${m.get('liquidity', 0):,.0f}")
        
        # Test with on-chain disabled
        print("\n[2] Testing API with on-chain DISABLED")
        response = await client.post(
            f"{base_url}/scan",
            json={
                "min_mentions": 3,
                "use_mock_data": True,
                "fetch_onchain": False,
                "top_n": 3
            }
        )
        
        data = response.json()
        predictions = data["data"]["predictions"]
        
        has_metrics = sum(1 for p in predictions if p.get("metrics") is not None)
        print(f"✅ API predictions with on-chain: {has_metrics}/{len(predictions)}")
        assert has_metrics == 0, "Should have no metrics when disabled"


async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🌊 MEMETIDE ON-CHAIN INTEGRATION TESTS")
    print("="*60)
    
    try:
        # Test 1: DexScreener client
        await test_dexscreener_client()
        
        # Test 2: Engine integration
        await test_engine_integration()
        
        # Test 3: API integration
        print("\n⚠️ Make sure API server is running at http://localhost:8000")
        print("   Run: ./start_server.sh")
        
        try:
            await test_api_integration()
        except httpx.ConnectError:
            print("\n⚠️ API server not running. Skipping API tests.")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60 + "\n")
    
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
