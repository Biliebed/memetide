# MemeTide API Documentation

FastAPI REST API for memecoin trend prediction.

---

## Quick Start

```bash
# Activate venv
cd ~/memetide
source venv/bin/activate

# Start API server
python api_server.py

# Server runs at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

---

## Endpoints

### `GET /`
Root endpoint with API info.

**Response:**
```json
{
  "name": "MemeTide API",
  "version": "1.0.0",
  "description": "AI-powered memecoin trend prediction",
  "docs": "/docs",
  "endpoints": {...}
}
```

---

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-07-03T10:30:00",
  "version": "1.0.0",
  "uptime_seconds": 123.45
}
```

---

### `POST /scan`
Run memecoin trend scan.

**Request Body:**
```json
{
  "min_mentions": 3,
  "top_n": 10,
  "use_mock_data": false,
  "fetch_onchain": true
}
```

**Parameters:**
- `min_mentions` (int, default: 3): Minimum mentions to consider a token
- `top_n` (int, optional): Return only top N predictions
- `use_mock_data` (bool, default: false): Use mock Twitter data for testing
- `fetch_onchain` (bool, default: true): Fetch on-chain metrics from DexScreener

**Response:**
```json
{
  "status": "success",
  "scan_id": "a1b2c3d4",
  "message": "Scan complete. Found 12 trending tokens.",
  "data": {
    "scan_id": "a1b2c3d4",
    "timestamp": "2026-07-03T10:30:00",
    "total_mentions": 156,
    "unique_tokens": 12,
    "duration_seconds": 3.42,
    "predictions": [
      {
        "token_symbol": "PEPE",
        "mention_count": 24,
        "mentions_per_hour": 18.2,
        "sentiment": {
          "positive": 0.875,
          "negative": 0.042,
          "neutral": 0.083,
          "compound": 0.812
        },
        "risk_level": "low",
        "confidence": "high",
        "score": 78.3,
        "metrics": {
          "contract_address": "0xa006454c220b80c4740944030a39bcdeb18f150b",
          "price_usd": 0.00120200,
          "market_cap": 1202950749,
          "liquidity": 601475375,
          "age_hours": 1467.0
        },
        "first_seen": "2026-07-03T09:15:00",
        "last_updated": "2026-07-03T10:30:00",
        "sample_tweets": [
          "$PEPE about to explode 🚀",
          "Everyone sleeping on $PEPE...",
          "$PEPE looks bullish af"
        ]
      }
    ]
  }
}
```

---

### `POST /scan/background`
Run scan in background (non-blocking).

Returns immediately with `scan_id`. Poll `/history` to get results.

**Request Body:**
```json
{
  "min_mentions": 3,
  "use_mock_data": false
}
```

**Response:**
```json
{
  "status": "processing",
  "scan_id": "bg-1720001234",
  "message": "Scan started in background. Poll /history for results.",
  "poll_url": "/history?limit=1"
}
```

---

### `GET /history`
Get scan history (paginated).

**Query Parameters:**
- `limit` (int, default: 10): Max results per page
- `offset` (int, default: 0): Pagination offset

**Response:**
```json
{
  "total": 25,
  "limit": 10,
  "offset": 0,
  "results": [
    {
      "scan_id": "a1b2c3d4",
      "timestamp": "2026-07-03T10:30:00",
      "unique_tokens": 12,
      "predictions": [...]
    }
  ]
}
```

---

### `GET /history/{scan_id}`
Get specific scan result by ID.

**Response:**
```json
{
  "status": "found",
  "data": {
    "scan_id": "a1b2c3d4",
    "timestamp": "2026-07-03T10:30:00",
    "predictions": [...]
  }
}
```

---

### `GET /stats`
Get API statistics.

**Response:**
```json
{
  "total_scans": 42,
  "total_tokens_analyzed": 347,
  "average_scan_duration": 3.21,
  "uptime_seconds": 7234.56
}
```

---

### `DELETE /history`
Clear scan history.

**Note:** Add authentication in production.

**Response:**
```json
{
  "status": "success",
  "message": "Cleared 25 scan results"
}
```

---

## Testing

### Python Test Script

```bash
# Start API server (terminal 1)
python api_server.py

# Run tests (terminal 2)
python test_api.py

# Print cURL examples
python test_api.py --curl
```

---

### cURL Examples

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Run Scan (Mock Data):**
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"min_mentions": 3, "use_mock_data": true, "top_n": 5}'
```

**Get History:**
```bash
curl http://localhost:8000/history?limit=5
```

**Get Stats:**
```bash
curl http://localhost:8000/stats
```

**Background Scan:**
```bash
curl -X POST http://localhost:8000/scan/background \
  -H "Content-Type: application/json" \
  -d '{"min_mentions": 2, "use_mock_data": true}'
```

---

## Interactive Docs

FastAPI provides auto-generated interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

You can test all endpoints directly in the browser.

---

## Error Handling

All endpoints return consistent error responses:

```json
{
  "status": "error",
  "message": "Scan failed: Connection timeout",
  "timestamp": "2026-07-03T10:30:00"
}
```

**HTTP Status Codes:**
- `200` - Success
- `404` - Resource not found
- `422` - Validation error
- `500` - Internal server error

---

## Rate Limiting

**Current:** No rate limiting (add in production).

**Recommended:**
- Free tier: 10 requests/minute
- Pro tier: 100 requests/minute
- API key required for production

---

## CORS

Current config allows all origins (`*`).

**Production config:**
```python
allow_origins=[
    "https://memetide.com",
    "https://okx.ai"
]
```

---

## Deployment

### Development
```bash
python api_server.py
```

### Production
```bash
# With Gunicorn + Uvicorn workers
gunicorn api_server:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

---

## OKX.AI Integration

MemeTide can be registered as an **Agent Service Provider (ASP)** on OKX.AI platform.

**Service URL:** `https://api.memetide.com/scan`

**Integration Steps:**
1. Deploy API to production server
2. Add OKX.AI authentication
3. Register on OKX.AI platform
4. Submit for approval

**Expected Request from OKX.AI:**
```json
{
  "user_id": "okx_user_123",
  "request": "Scan trending memecoins",
  "min_mentions": 5
}
```

**Response to OKX.AI:**
```json
{
  "status": "success",
  "message": "Found 8 trending memecoins",
  "predictions": [...]
}
```

---

## Performance

**Benchmarks (mock data):**
- Scan duration: ~3-5 seconds
- Tokens processed: 10-20 per scan
- Memory usage: ~50-100 MB
- Concurrent requests: Up to 10 (increase workers for more)

---

## Monitoring

Add monitoring in production:

```python
from prometheus_client import Counter, Histogram

scan_counter = Counter('memetide_scans_total', 'Total scans')
scan_duration = Histogram('memetide_scan_duration_seconds', 'Scan duration')
```

---

## Security

**TODO for production:**
- [ ] Add API key authentication
- [ ] Implement rate limiting
- [ ] Add request validation
- [ ] Sanitize user inputs
- [ ] Enable HTTPS only
- [ ] Add CORS restrictions
- [ ] Implement audit logging

---

## Support

**Issues:** https://github.com/Biliebed/memetide/issues  
**Docs:** https://github.com/Biliebed/memetide/blob/main/API.md

---

**Built for OKX.AI Genesis Hackathon 2026** 🚀
