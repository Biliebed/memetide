# 🚀 Quick Deployment Guide

Complete step-by-step deployment to production.

---

## Part 1: Push to GitHub (2 minutes)

### Option A: GitHub CLI (Recommended)

```bash
cd ~/memetide

# Install GitHub CLI if not installed
# Ubuntu/Debian:
sudo apt install gh

# Login to GitHub
gh auth login
# Choose: GitHub.com → HTTPS → Login with browser

# Push to GitHub
git push -u origin main

# Create repo if doesn't exist
gh repo create memetide --public --source=. --remote=origin --push
```

### Option B: SSH Key

```bash
cd ~/memetide

# Generate SSH key if needed
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub
# Add this to GitHub Settings → SSH Keys

# Change remote to SSH
git remote remove origin
git remote add origin git@github.com:Biliebed/memetide.git

# Push
git push -u origin main
```

### Option C: Personal Access Token

```bash
cd ~/memetide

# Create token: GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
# Scopes: repo (all)

# Push with token
git push https://YOUR_TOKEN@github.com/Biliebed/memetide.git main
```

---

## Part 2: Deploy to Railway (3 minutes)

### Step 1: Create Railway Account

1. Go to https://railway.app
2. Sign up with GitHub account
3. Authorize Railway

### Step 2: Deploy Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose **Biliebed/memetide**
4. Railway auto-detects:
   - Python runtime
   - Procfile
   - railway.json
5. Click **"Deploy Now"**

### Step 3: Get URL

1. Wait ~2 minutes for build
2. Go to **Settings → Domains**
3. Click **"Generate Domain"**
4. Get URL: `https://memetide-production-XXXX.up.railway.app`

### Step 4: Test Deployment

```bash
# Test health endpoint
curl https://your-app.up.railway.app/health

# Test dashboard
curl https://your-app.up.railway.app/ -I

# Test scan
curl -X POST https://your-app.up.railway.app/scan \
  -H "Content-Type: application/json" \
  -d '{"min_mentions": 3, "use_mock_data": true}'
```

---

## Alternative: Deploy to Render

### Step 1: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub

### Step 2: Deploy

1. Click **"New +"** → **"Web Service"**
2. Connect GitHub repo: **Biliebed/memetide**
3. Settings:
   - **Name:** memetide
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn api_server:app --host 0.0.0.0 --port $PORT`
4. Click **"Create Web Service"**

### Step 3: Get URL

- URL: `https://memetide.onrender.com`
- Free tier: 750 hours/month

---

## Alternative: Deploy to Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy
cd ~/memetide
fly launch --name memetide --region sin

# Get URL
fly status
```

---

## Part 3: Update README with Live URL

```bash
cd ~/memetide

# Edit README.md
nano README.md

# Add at top:
## 🌐 Live Demo

**Dashboard:** https://your-app.railway.app  
**API Docs:** https://your-app.railway.app/docs

# Commit and push
git add README.md
git commit -m "Add live demo URL"
git push
```

---

## Part 4: Test Production

### Health Check

```bash
curl https://your-app.railway.app/health
```

Expected:
```json
{
  "status": "healthy",
  "timestamp": "2026-07-03T10:30:00",
  "version": "1.0.0",
  "uptime_seconds": 123.45
}
```

### Dashboard Test

1. Open https://your-app.railway.app in browser
2. Click "Scan" (mock data)
3. Verify results load
4. Test dark mode toggle
5. Test export button
6. Test history

### API Test

```bash
# Run scan
curl -X POST https://your-app.railway.app/scan \
  -H "Content-Type: application/json" \
  -d '{
    "min_mentions": 3,
    "use_mock_data": true,
    "fetch_onchain": true,
    "top_n": 5
  }' | jq .

# Get stats
curl https://your-app.railway.app/stats | jq .

# Get history
curl https://your-app.railway.app/history?limit=5 | jq .
```

---

## Troubleshooting

### Build Fails

**Error:** `requirements.txt not found`
- Fix: Check file exists, push to GitHub

**Error:** `Port not available`
- Fix: Ensure `api_server.py` uses `PORT` env variable

**Error:** `Module not found`
- Fix: Add missing package to `requirements.txt`

### Runtime Errors

**Error:** `Health check failing`
```bash
# Check logs
railway logs  # or fly logs, render logs
```

**Error:** `Static files not loading`
- Fix: Ensure `static/` directory pushed to GitHub
- Check `app.mount("/static", ...)` in api_server.py

**Error:** `CORS issues`
- Fix: Already configured with `allow_origins=["*"]`

### Deployment Too Slow

**Railway/Render free tier:**
- Cold start: ~10-30 seconds
- Solution: Upgrade to paid plan ($5/mo) or keep alive with cron

---

## Part 5: Submit to OKX.AI Hackathon

### Submission Checklist

- ✅ GitHub repo public
- ✅ README with live demo URL
- ✅ Working dashboard deployment
- ✅ API endpoints functional
- ✅ 90-second demo video
- ✅ Project description

### Demo Video Script

**Record with:** OBS Studio, Loom, or browser screen record

```
[0-10s] Introduction
- "MemeTide - AI memecoin trend predictor"
- Show landing page

[10-30s] Core Feature Demo
- Run scan with mock data
- Show results with confidence badges
- Point out sample tweets
- Highlight on-chain metrics

[30-45s] Advanced Features
- Toggle dark mode
- Export results to JSON
- View scan history

[45-60s] Technical Stack
- FastAPI + DexScreener
- Twitter sentiment analysis
- Risk scoring

[60-75s] Value Proposition
- Finance copilot for traders
- Social buzz monitoring
- Zero-cost deployment

[75-90s] Call to Action
- GitHub link
- Live demo link
- Thank you
```

### Submission Form

**Project Name:** MemeTide

**Tagline:** AI-powered memecoin trend predictor with sentiment analysis

**Description:**
```
MemeTide analyzes Twitter/X sentiment and on-chain metrics to predict 
trending memecoins. Built with FastAPI, TextBlob sentiment analysis, 
and DexScreener API. Features include:

- Real-time Twitter monitoring
- AI sentiment scoring
- On-chain metrics (price, liquidity, market cap)
- Risk assessment & scam detection
- Web dashboard with dark mode
- REST API with 8 endpoints

Perfect for traders who want to catch memecoin trends early while 
avoiding scams and rugs.

Targets: Finance Copilot + Social Buzz awards
```

**Category:** Finance Copilot, Social Buzz

**Links:**
- GitHub: https://github.com/Biliebed/memetide
- Live Demo: https://your-app.railway.app
- Video: https://youtu.be/YOUR_VIDEO_ID

**Tech Stack:** Python, FastAPI, TextBlob, DexScreener API, Chart.js

**Team Size:** Solo

---

## Post-Deployment Monitoring

### Check Uptime

```bash
# Railway
railway status

# Render
curl https://memetide.onrender.com/health

# Fly.io
fly status
```

### View Logs

```bash
# Railway
railway logs --tail

# Render: Dashboard → Logs

# Fly.io
fly logs
```

### Update Deployment

```bash
# Make changes locally
git add .
git commit -m "Update feature X"
git push

# Auto-deploys on Railway/Render
# Fly.io: fly deploy
```

---

## Cost Summary

| Platform | Free Tier | Auto-Deploy | Cold Start |
|----------|-----------|-------------|------------|
| Railway | 500 hrs/mo | ✅ Yes | ~5s |
| Render | 750 hrs/mo | ✅ Yes | ~10s |
| Fly.io | 3 VMs | ✅ Yes | ~3s |

**Recommended:** Railway (easiest setup, good free tier)

---

## Success Criteria

✅ GitHub repo pushed  
✅ Live URL accessible  
✅ Dashboard loads  
✅ API endpoints respond  
✅ README updated with live URL  
✅ Demo video recorded  
✅ Hackathon submission complete  

---

**Total Time:** ~10-15 minutes from start to live deployment

**Support:** Check platform docs or ask for help!
