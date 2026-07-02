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
✅ **Risk assessment** - Detects scams, rugs, and honeypots  
✅ **Confidence scoring** - Ranks predictions by reliability  
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

## API Usage (Coming Soon)

```python
from src import MemeTideEngine

# Initialize engine
engine = MemeTideEngine(use_mock_data=False)

# Run scan
result = await engine.scan(min_mentions=3)

# Get high confidence predictions
for pred in result.get_high_confidence():
    print(f"🔥 ${pred.token_symbol} - Score: {pred.score}/100")
```

---

## Architecture

**Core Components:**

- **Scraper** (`src/scraper.py`) - Twitter/X data collection
- **Analyzer** (`src/analyzer.py`) - Sentiment analysis & token extraction
- **Risk Scorer** (`src/risk.py`) - Scam detection & confidence calculation
- **Engine** (`src/engine.py`) - Orchestrates full scan pipeline
- **Models** (`src/models.py`) - Data structures

**Tech Stack:**

- Python 3.10+
- TextBlob (sentiment analysis)
- BeautifulSoup4 (web scraping)
- httpx (async HTTP)
- FastAPI (API server - coming soon)

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

**v1.1 (Next):**
- [ ] FastAPI endpoint
- [ ] OKX.AI platform listing
- [ ] On-chain metrics (DexScreener integration)
- [ ] Real-time alerts

**v2.0 (Future):**
- [ ] Multi-chain support (Solana, Base, etc.)
- [ ] Historical backtesting
- [ ] Telegram bot
- [ ] Premium features (price predictions, whale tracking)

---

## Demo Video

📹 [Watch 90-second demo](https://youtu.be/XXX) (Coming soon)

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
