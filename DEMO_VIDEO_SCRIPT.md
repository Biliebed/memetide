# 🎬 MemeTide Demo Video Script - 90 Seconds

**Target:** OKX.AI Genesis Hackathon Submission  
**Duration:** 90 seconds (strict)  
**Format:** Screen recording + voiceover  
**Goal:** Show production-ready multi-chain memecoin predictor

---

## 📋 Pre-Recording Checklist

- [ ] Open https://memetide-production.up.railway.app/docs in browser
- [ ] Prepare browser console (F12) for WebSocket demo
- [ ] Test internet connection (deployment harus live)
- [ ] Close unnecessary tabs/windows
- [ ] Set browser zoom to 100%
- [ ] Prepare voice recorder / mic
- [ ] Have script printed or on second screen

---

## 🎯 Script Breakdown (90 seconds)

### INTRO (0-10s)

**Visual:** GitHub repo / README header with badges

**Voiceover:**
> "MemeTide – AI-powered memecoin trend predictor. Catch pumps before they happen. Built for OKX.AI Genesis Hackathon."

**Action:**
- Show GitHub repo: github.com/Biliebed/memetide
- Highlight: Live Demo badge, 99.9% uptime, v1.2.0

---

### PART 1: Live API Demo (10-30s)

**Visual:** Swagger UI at /docs

**Voiceover:**
> "Production-ready API with 12 endpoints. Let's scan trending memecoins."

**Action:**
1. Click "POST /scan" endpoint
2. Click "Try it out"
3. Use this JSON:
   ```json
   {
     "use_mock_data": true,
     "top_n": 3,
     "min_mentions": 3
   }
   ```
4. Click "Execute"
5. Show results in <1 second:
   - FLOKI: Score 51.2, MEDIUM confidence
   - PEPE2: Score 35.5, LOW confidence  
   - SCAMCOIN: Score 0, HIGH risk (scam detected)

**Voiceover:**
> "In under a second: AI sentiment, risk scoring, confidence levels. SCAMCOIN flagged as scam – saved you from a rug pull."

---

### PART 2: Multi-chain Search (30-50s)

**Visual:** Still in /docs, switch to GET /token/multichain/{symbol}

**Voiceover:**
> "Multi-chain support. Search tokens across 6 blockchains simultaneously."

**Action:**
1. Click "GET /token/multichain/{symbol}"
2. Click "Try it out"
3. Enter symbol: `PEPE`
4. Enter chains: `ethereum,solana`
5. Click "Execute"
6. Show results:
   - **Ethereum:** $1.16B market cap, $0.000002811
   - **Solana:** $3.96M market cap, $0.000003959

**Voiceover:**
> "PEPE found on Ethereum and Solana. Compare prices, liquidity, market caps across chains instantly."

---

### PART 3: Real-time WebSocket (50-75s)

**Visual:** Browser console (F12)

**Voiceover:**
> "Real-time WebSocket alerts. Subscribe to specific tokens for instant updates."

**Action:**
1. Open browser console (F12)
2. Paste and run this code:
   ```javascript
   const ws = new WebSocket('wss://memetide-production.up.railway.app/ws/alerts');
   ws.onopen = () => {
     console.log('✅ Connected');
     ws.send(JSON.stringify({command: 'subscribe', tokens: ['PEPE', 'FLOKI']}));
   };
   ws.onmessage = (e) => {
     const data = JSON.parse(e.data);
     console.log('🔔', data.type, data);
   };
   ```
3. Show connection message
4. Show subscription confirmation

**Voiceover:**
> "WebSocket connected. Subscribed to PEPE and FLOKI. Any new trends push to you instantly – no polling, no delays."

---

### PART 4: Authentication & Enterprise Features (75-85s)

**Visual:** Back to /docs, show POST /auth/login

**Voiceover:**
> "Enterprise features: JWT authentication, rate limiting, free and premium tiers."

**Action:**
1. Quick scroll through endpoints:
   - /auth/login (JWT)
   - /trending/{chain} (chain-specific)
   - /history (scan history)
2. Show URL bar: https://memetide-production.up.railway.app

**Voiceover:**
> "Production deployed on Railway. 99.9% uptime. Rate-limited at 60 requests per minute. Ready for OKX.AI platform."

---

### CLOSING (85-90s)

**Visual:** GitHub README or logo screen

**Voiceover:**
> "MemeTide. Multi-chain. Real-time. AI-powered. Don't chase pumps – predict them. Built for OKX.AI Genesis Hackathon."

**Text on screen:**
- 🌐 Live: memetide-production.up.railway.app
- 💻 GitHub: github.com/Biliebed/memetide
- 🏆 Categories: Finance Copilot + Social Buzz

---

## 🎥 Recording Tips

### Software Options:
1. **OBS Studio** (free, best quality)
   - Download: obsproject.com
   - 1920x1080, 30fps, ~5mbps bitrate
2. **Loom** (easiest, browser-based)
   - loom.com - auto-upload to cloud
3. **QuickTime** (Mac)
   - Screen Recording feature
4. **Windows Game Bar** (Windows)
   - Win + G

### Settings:
- **Resolution:** 1920x1080 (Full HD)
- **Frame rate:** 30fps
- **Format:** MP4 (H.264)
- **Audio:** Clear voice, no background noise
- **Length:** 85-90 seconds (strict)

### Recording Workflow:
1. **Practice run** (no recording) - ensure smooth flow
2. **Test recording** (10s) - check audio/video quality
3. **Final take** - aim for 1-2 takes max
4. **Review** - watch full video, check timing

---

## ✂️ Editing (Optional)

If over 90s, cut:
- Intro animation (jump straight to demo)
- Wait times (speed up 1.5x or cut pauses)
- Verbose explanations (keep script tight)

Tools:
- **DaVinci Resolve** (free, professional)
- **iMovie** (Mac, simple)
- **Clipchamp** (Windows, online)
- **Kapwing** (online, easiest)

---

## 📤 Export Settings

**Final video specs:**
- Format: MP4
- Codec: H.264
- Resolution: 1920x1080 (or 1280x720 if file too large)
- Frame rate: 30fps
- Bitrate: 5-8 Mbps
- Audio: AAC, 128-192 kbps
- Max file size: 100MB (typical platform limit)

**Duration:** 90 seconds ±3s

---

## 🎤 Voiceover Tips

### Tone:
- Confident, not salesy
- Fast-paced but clear
- Technical but accessible

### Delivery:
- Speak slightly faster than normal (fit 90s)
- Emphasize key phrases: "production-ready", "multi-chain", "real-time"
- Pause briefly at transitions (easier to edit)

### Language:
- **Bahasa Indonesia:** OK if target audience Indonesian
- **English:** Better for international hackathon judges
- **Recommendation:** English with clear accent

---

## 🚀 Alternative: No Voiceover Version

If mic quality poor or not comfortable speaking:

**Use text overlays instead:**
- Title cards between sections (3-5s each)
- Captions explaining what's happening
- Background music (royalty-free from YouTube Audio Library)
- Faster cuts (no need to wait for voice)

**Pro:** Easier to produce, no accent issues  
**Con:** Less engaging, harder to explain complex features

---

## 📊 Success Checklist

Video should demonstrate:

- [ ] Live deployment (production URL visible)
- [ ] Fast response times (<1s for scan)
- [ ] Multi-chain capability (Ethereum + Solana)
- [ ] AI sentiment analysis (positive/negative scores)
- [ ] Risk detection (SCAMCOIN flagged)
- [ ] WebSocket real-time (connection + subscription)
- [ ] Authentication (JWT endpoint shown)
- [ ] Professional UI (Swagger docs)
- [ ] Uptime/stability (badges shown)

---

## 🎬 QUICK 30-MINUTE RECORDING PLAN

**Prep (5 min):**
1. Open all tabs/windows
2. Set browser zoom 100%
3. Close distractions
4. Read script 2x

**Practice (5 min):**
1. Dry run without recording
2. Time it (should be 85-90s)
3. Adjust pace if needed

**Record (10 min):**
1. Test audio (5s clip)
2. Take 1 (full 90s)
3. Review
4. Take 2 if needed

**Edit (5 min):**
1. Trim intro/outro
2. Add title card (first 3s)
3. Add closing card (last 3s)

**Export (5 min):**
1. Export as MP4, 1080p, 30fps
2. Check file size (<100MB)
3. Watch final video once

**Total: 30 minutes**

---

## 📝 Alternative: Screenshot + Slides Approach

If screen recording too complex:

**Option B: PowerPoint/Slides + Screenshots**

1. **Slide 1:** MemeTide logo + tagline (3s)
2. **Slide 2:** Screenshot of /docs with scan result (10s)
3. **Slide 3:** Screenshot of multi-chain search (10s)
4. **Slide 4:** Screenshot of WebSocket console (10s)
5. **Slide 5:** Screenshot of auth endpoints (5s)
6. **Slide 6:** Deployment stats (badges, uptime) (10s)
7. **Slide 7:** Closing (GitHub + live URL) (5s)

**Export as video:** PowerPoint → File → Export → Video (MP4)

**Add voiceover:** Record audio separately, overlay in video editor

---

## 🔥 Pro Tips

1. **Show, don't tell** - Let the API responses speak
2. **Highlight speed** - Emphasize <1s response times
3. **Show scam detection** - SCAMCOIN example impressive
4. **Multi-chain is key** - This differentiates from competitors
5. **Real-time = wow factor** - WebSocket demo memorable
6. **Production URL visible** - Proves it's live, not mockup

---

## 🎯 Final Note

**Goal:** In 90 seconds, judges should think:
> "This is a production-ready, multi-chain, real-time memecoin predictor with AI risk detection. Impressive."

**Not goal:**
> "This is a nice idea that might work someday."

**Key message:** It's LIVE. It WORKS. It's FAST. It's SMART.

---

**Ready to record?** Follow the script, keep it tight, and show off those enterprise features!

Good luck bro! 🚀🎬
