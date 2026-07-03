# On-Chain Metrics Integration

MemeTide integrates with DexScreener API to fetch real-time on-chain data for memecoins.

---

## Features

✅ **Price (USD)** - Current token price  
✅ **Market Cap** - Fully diluted valuation  
✅ **Liquidity** - Total liquidity across pairs  
✅ **Token Age** - Hours since pair creation  
✅ **Contract Address** - Verified contract address  
✅ **Automatic Caching** - 60-second TTL to reduce API calls  
✅ **Batch Fetching** - Parallel requests for multiple tokens  

---

## Data Source

**API:** DexScreener (https://dexscreener.com)  
**Rate Limit:** 300 requests/minute  
**Cost:** Free (no API key required)  
**Coverage:** Ethereum, BSC, Polygon, Solana, Base, and 50+ chains  

---

## Usage

### CLI

**Enabled by default:**
```bash
python cli.py
```

**Disable on-chain metrics (faster):**
```bash
# Not available via CLI flag yet
# Edit cli.py and set fetch_onchain=False
```

### API

**Enabled by default:**
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"min_mentions": 3, "use_mock_data": true}'
```

**Disable on-chain metrics:**
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"min_mentions": 3, "use_mock_data": true, "fetch_onchain": false}'
```

### Python SDK

```python
from src.engine import MemeTideEngine

# With on-chain metrics (default)
engine = MemeTideEngine(use_mock_data=True, fetch_onchain=True)
result = await engine.scan(min_mentions=3)

# Without on-chain metrics
engine = MemeTideEngine(use_mock_data=True, fetch_onchain=False)
result = await engine.scan(min_mentions=3)
```

---

## Response Format

**With on-chain metrics:**
```json
{
  "token_symbol": "PEPE",
  "score": 78.3,
  "metrics": {
    "contract_address": "0xA006454c220b80c4740944030A39bCDEb18f150B",
    "price_usd": 0.00120200,
    "market_cap": 1202950749,
    "liquidity": 601475375,
    "age_hours": 1467.0
  }
}
```

**Without on-chain metrics:**
```json
{
  "token_symbol": "PEPE",
  "score": 78.3,
  "metrics": null
}
```

---

## Performance

**With on-chain:**
- Scan duration: ~0.5-1.5 seconds (depends on token count)
- Network calls: 1 per token (cached for 60s)

**Without on-chain:**
- Scan duration: ~0.01-0.05 seconds
- Network calls: 0

**Recommendation:** Enable for production, disable for rapid testing.

---

## Caching

DexScreener client caches results for 60 seconds:

```python
from src.dexscreener import DexScreenerClient

client = DexScreenerClient()

# First call: hits API
metrics1 = await client.get_metrics("PEPE")  # ~200ms

# Second call: returns cached (within 60s)
metrics2 = await client.get_metrics("PEPE")  # ~0.1ms
```

Adjust TTL:
```python
client = DexScreenerClient()
client.cache_ttl = 120  # 2 minutes
```

---

## Token Matching

DexScreener returns multiple pairs per symbol. The client selects the best pair using this logic:

1. **Filter:** Symbol must match exactly (case-insensitive)
2. **Filter:** Minimum $1,000 liquidity
3. **Sort:** Highest liquidity wins

**Example:** Searching "PEPE" returns:
- ✅ PEPE/WETH on Ethereum ($601M liquidity) → Selected
- ❌ PEPE/USDC on BSC ($5k liquidity) → Filtered out (low liquidity)
- ❌ PEPEWIFHAT/WETH ($10M liquidity) → Filtered out (symbol mismatch)

---

## Error Handling

**Token not found:**
```python
metrics = await client.get_metrics("FAKECOIN")
# Returns: None
```

**API timeout:**
```python
client = DexScreenerClient(timeout=5)  # 5 second timeout
metrics = await client.get_metrics("PEPE")
# Returns: None if timeout
```

**Network error:**
```python
# Prints warning, returns None
# [DexScreener] Error fetching PEPE: Connection timeout
```

---

## Testing

```bash
# Test DexScreener client directly
cd ~/memetide/src
python dexscreener.py

# Test full integration
cd ~/memetide
python test_onchain.py
```

**Expected output:**
```
============================================================
🌊 MEMETIDE ON-CHAIN INTEGRATION TESTS
============================================================

TEST 1: DexScreener Client
✅ PEPE: $0.00120200, Liq: $601,475,375
✅ FLOKI: $0.00002301, Liq: $7,617,060
✅ DOGE: $0.08386000, Liq: $838,435,299

TEST 2: Engine Integration
✅ Predictions with on-chain data: 3/3

TEST 3: API Integration
✅ API predictions with on-chain: 3/3

✅ ALL TESTS PASSED
============================================================
```

---

## Limitations

1. **Rate Limits:** 300 req/min shared across all users
2. **Coverage:** Only tokens with DEX liquidity (no CEX-only tokens)
3. **Latency:** Adds ~100-300ms per token
4. **Accuracy:** Data from DEX pairs only (may differ from CEX prices)

---

## Future Improvements

**v1.1:**
- [ ] Support custom DexScreener API key
- [ ] Add CoinGecko as fallback
- [ ] Cache to Redis for multi-instance deployments
- [ ] Historical price data

**v2.0:**
- [ ] Multi-chain aggregation
- [ ] Holder count (via Etherscan API)
- [ ] Whale wallet tracking
- [ ] Price prediction based on historical on-chain data

---

## API Reference

See [DexScreener Docs](https://docs.dexscreener.com/api/reference) for full API details.

**Endpoints used:**
- `GET /latest/dex/search?q={symbol}` - Search by symbol

---

**Built for OKX.AI Genesis Hackathon 2026** 🚀
