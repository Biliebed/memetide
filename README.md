# MemeTide 🌊

**Catch memecoin trends before they explode**

AI-powered memecoin trend predictor for OKX.AI Genesis Hackathon

---

## What is MemeTide?

MemeTide monitors crypto Twitter in real-time, using AI sentiment analysis to detect trending memecoins **before** they pump.

Stop chasing pumps. Start predicting them.

---

## Features

✅ **Real-time Twitter monitoring** - Tracks thousands of crypto tweets  
✅ **AI sentiment analysis** - Understands crypto slang & hype  
✅ **On-chain metrics** - Price, liquidity, market cap from DexScreener  
✅ **Risk assessment** - Detects scams, rugs, and honeypots  
✅ **Confidence scoring** - Ranks predictions by reliability  
✅ **REST API** - FastAPI server with 8 endpoints  
✅ **CLI tool** - Quick terminal-based scanning  
✅ **Zero setup** - Works out of the box with mock data  

---

## Quick Start

```bash
# Clone repo
git clone https://github.com/Biliebed/memetide
cd memetide

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run scan
python cli.py
```

**Output:**
```
🌊 MEMETIDE SCAN RESULTS

📊 TOP 3 PREDICTIONS:

1. 🔥 $PEPE2
   Score: 78.3/100
   Mentions: 24 (18.2/hr)
   Sentiment: 87.5% positive
   Risk: LOW
   Confidence: HIGH

2. ⚠️ $FLOKI
   Score: 53.1/100
   Mentions: 9 (5.0/hr)
   Sentiment: 76.9% positive
   Risk: LOW
   Confidence: MEDIUM

3. ❌ $SCAMCOIN
   Score: 0.0/100
   Mentions: 3 (2.4/hr)
   Sentiment: 0.0% positive
   Risk: HIGH
   Confidence: LOW
```

---

## How It Works

```
Twitter/X Crypto Posts
        ↓
   [1. Scrape]
        ↓
  Token Extraction ($PEPE, $FLOKI, etc.)
        ↓
   [2. Analyze]
   ├─ Sentiment (AI-powered)
   ├─ Volume (mentions/hour)
   ├─ Risk (scam detection)
   └─ Engagement (likes, RTs)
        ↓
   [3. Score]
   ├─ Volume factor (0-30 pts)
   ├─ Sentiment factor (0-30 pts)
   ├─ Consistency (0-20 pts)
   └─ Risk penalty (-40 pts)
        ↓
   [4. Rank]
        ↓
  🔥 HIGH | ⚠️ MEDIUM | ❌ LOW
```

---

## CLI Usage

```bash
# Basic scan
python cli.py

# Show top 5 only
python cli.py --top 5

# JSON output
python cli.py --json

# Use real Twitter data (requires Nitter)
python cli.py --real

# Set minimum mentions threshold
python cli.py --min-mentions 5
```

---

## API Usage

**Start API Server:**

```bash
./start_server.sh

# Or manually:
python api_server.py
```

**Interactive Docs:** http://localhost:8000/docs

**Example API Call:**

```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"min_mentions": 3, "use_mock_data": true}'
```

**Python Client:**

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/scan",
        json={"min_mentions": 3, "use_mock_data": True}
    )
    result = response.json()
    print(f"Found {result['data']['unique_tokens']} trending tokens")
```

**Full API Docs:** [API.md](API.md) | [API Quick Start](API_QUICKSTART.md)

---

## Architecture

**Core Components:**

- **Scraper** (`src/scraper.py`) - Twitter/X data collection
- **Analyzer** (`src/analyzer.py`) - Sentiment analysis & token extraction
- **DexScreener** (`src/dexscreener.py`) - On-chain metrics (price, liquidity, age)
- **Risk Scorer** (`src/risk.py`) - Scam detection & confidence calculation
- **Engine** (`src/engine.py`) - Orchestrates full scan pipeline
- **API Server** (`api_server.py`) - FastAPI REST API
- **Models** (`src/models.py`) - Data structures

**Tech Stack:**

- Python 3.10+
- FastAPI + Uvicorn (REST API)
- TextBlob (sentiment analysis)
- BeautifulSoup4 (web scraping)
- httpx (async HTTP for DexScreener)
- DexScreener API (on-chain data)

---

## Scoring Algorithm

**Score Components (0-100):**

1. **Volume (30%)** - Mentions per hour
2. **Sentiment (30%)** - Positive/negative ratio
3. **Consistency (20%)** - Volume + sentiment alignment
4. **Risk Penalty (up to -40%)** - Scam indicators

**Risk Factors:**

- Negative sentiment (scam, rug, honeypot keywords)
- Excessive hype (pump & dump indicator)
- Low engagement (bot activity)
- New token (<24h old)
- Low liquidity (<$10k)

**Confidence Levels:**

- 🔥 **HIGH** (70-100): Strong signal, act now
- ⚠️ **MEDIUM** (40-69): Promising, monitor
- ❌ **LOW** (0-39): Weak signal, avoid

---

## Real-World Performance

*Demo data shows detection capability. Real performance TBD.*

**Hypothetical Example:**

- MemeTide detected $PEPE2 trending 2 hours before 50x pump
- Sentiment: 87% positive
- Mentions spiked from 5/hr → 120/hr
- Risk: LOW (legitimate contract, good liquidity)

---

## OKX.AI Integration

MemeTide is built as an **Agent Service Provider (ASP)** for OKX.AI platform.

**Service Model:**

- **Input:** User request "Scan trending memecoins"
- **Process:** Real-time Twitter scan + AI analysis
- **Output:** Ranked predictions with confidence scores

**Pricing (proposed):**

- Free tier: 3 scans/day
- Pro tier: Unlimited scans + alerts ($9.99/month)
- API access: $0.10 per scan

---

## Roadmap

**v1.0 (Current):**
- ✅ Twitter scraping (Nitter)
- ✅ AI sentiment analysis
- ✅ Risk scoring
- ✅ CLI tool
- ✅ FastAPI endpoint
- ✅ Background task support
- ✅ Scan history & stats
- ✅ On-chain metrics (DexScreener)

**v1.1 (Next):**
- [ ] OKX.AI platform listing
- [ ] Real-time alerts (WebSocket)
- [ ] Authentication & rate limiting
- [ ] Historical price tracking

**v2.0 (Future):**
- [ ] Multi-chain support (Solana, Base, etc.)
- [ ] Historical backtesting
- [ ] Telegram bot
- [ ] Premium features (price predictions, whale tracking)

---

## Demo Video

📹 [Watch 90-second demo](https://youtu.be/XXX) (Coming soon)

**Live API Demo:** [Coming soon after deployment]

---

## Deployment

**Quick Deploy (5 min):** See [DEPLOY_QUICK.md](DEPLOY_QUICK.md)

**Full Guide:** See [DEPLOY.md](DEPLOY.md) for Railway, Render, Fly.io, Docker options.

**Deployment Configs:**
- ✅ `Dockerfile` - Docker container
- ✅ `Procfile` - Heroku/Railway
- ✅ `railway.json` - Railway config
- ✅ `runtime.txt` - Python version

---

## Hackathon Submission

**OKX.AI Genesis Hackathon**  
**Category:** Finance Copilot + Social Buzz  
**Team:** Biliebed  
**Submitted:** July 2026

---

## Contributing

This project is open source under MIT license.

Pull requests welcome!

---

## Disclaimer

⚠️ **For educational purposes only.**

MemeTide is a research project demonstrating AI-powered trend analysis. It does NOT provide financial advice. Memecoin trading is highly risky. DYOR.

---

## Links

- **GitHub:** https://github.com/Biliebed/memetide
- **Twitter:** [Coming soon]
- **OKX.AI Listing:** [Coming soon]

---

## License

MIT License - See LICENSE file

---

**Built for OKX.AI Genesis Hackathon 2026** 🚀

*Don't chase pumps. Predict them. MemeTide.* 🌊
