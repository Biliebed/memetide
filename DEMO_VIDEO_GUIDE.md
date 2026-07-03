# 🎬 MemeTide Demo Video Guide

Complete guide untuk record demo video 90 detik yang powerful.

---

## 🎯 Video Requirements

**Duration:** 90 seconds (max)  
**Format:** MP4 or MOV (1080p recommended)  
**Audio:** Clear voice or background music  
**Platform:** YouTube (unlisted or public)  

---

## 🛠️ Recording Tools

### Option 1: OBS Studio (Recommended)

**Download:** https://obsproject.com/download

**Setup:**
```bash
# Ubuntu/Linux
sudo apt install obs-studio

# Launch
obs
```

**Settings:**
- Video: 1920x1080, 30fps
- Audio: Desktop + Microphone (optional)
- Output: MP4, High Quality

### Option 2: Browser-Based (Easiest)

**Loom:** https://loom.com (free, 5 min limit)
- Chrome extension
- Record tab + camera (optional)
- Auto-uploads to cloud

**Screen Studio:** https://screen.studio (paid, but beautiful)

### Option 3: Built-in Tools

**Linux (FFmpeg):**
```bash
# Record screen
ffmpeg -f x11grab -s 1920x1080 -i :0.0 -r 30 demo.mp4

# Stop with Ctrl+C
```

**Mac:**
- QuickTime Player → File → New Screen Recording

**Windows:**
- Xbox Game Bar (Win + G)

---

## 📝 Demo Script (90 seconds)

### Scene 1: Introduction (0-15s)

**Screen:** Dashboard landing page at http://localhost:8000

**Voiceover:**
```
"Hi, I'm showcasing MemeTide - an AI-powered memecoin trend predictor 
built for the OKX.AI Genesis Hackathon. It helps traders catch 
trending memecoins early while avoiding scams."
```

**Actions:**
- Show clean landing page
- Point to title "MemeTide"
- Briefly show tagline

**Visual Elements:**
- Gradient purple background
- Clean UI
- Professional look

---

### Scene 2: Core Functionality (15-35s)

**Screen:** Run scan and show results

**Voiceover:**
```
"MemeTide scans Twitter for trending tokens, analyzes sentiment, 
and fetches real-time on-chain data from DexScreener."
```

**Actions:**
1. Click "🚀 Scan" button (leave defaults)
2. Show loading spinner (~1 second)
3. Results appear with predictions

**Point Out:**
- Confidence badges (🔥 High, ⚠️ Medium, ❌ Low)
- Score out of 100
- Mention count with hourly rate
- Sentiment percentage

**Timing:** 20 seconds total

---

### Scene 3: Detailed View (35-55s)

**Screen:** Scroll through prediction cards

**Voiceover:**
```
"Each token shows on-chain metrics like price, market cap, and 
liquidity, plus sample tweets sorted by engagement. Risk scoring 
helps avoid scams and rugs."
```

**Actions:**
1. Scroll to first token card
2. Highlight on-chain metrics section:
   - Price: $0.00002301
   - Market Cap: $94M
   - Liquidity: $7.6M
3. Show sample tweets section
4. Point to risk level (LOW/MEDIUM/HIGH)

**Timing:** 20 seconds

---

### Scene 4: Advanced Features (55-70s)

**Screen:** Show dark mode, export, history

**Voiceover:**
```
"Dark mode for late-night trading. Export results to JSON for 
analysis. View scan history to track trends over time."
```

**Actions:**
1. Click 🌙 moon icon (toggle dark mode) - 3 seconds
2. Toggle back to light mode
3. Click 💾 Export button (JSON downloads) - 3 seconds
4. Click 📜 History button (show past scans) - 3 seconds
5. Click back to results

**Timing:** 15 seconds

---

### Scene 5: Technical Details (70-85s)

**Screen:** Show API docs briefly (http://localhost:8000/docs)

**Voiceover:**
```
"Built with FastAPI and Python. Uses DexScreener for on-chain data, 
TextBlob for sentiment analysis. Completely free to deploy on 
Railway or Render. Zero external costs."
```

**Actions:**
1. Switch to /docs tab (2 seconds)
2. Show endpoints list briefly
3. Scroll quickly through Swagger UI

**Timing:** 15 seconds

---

### Scene 6: Closing (85-90s)

**Screen:** Back to dashboard with results

**Voiceover:**
```
"Perfect for Finance Copilot and Social Buzz categories. 
Check it out at github.com/Biliebed/memetide. Thank you!"
```

**Actions:**
- Show final results screen
- Display GitHub URL (optional: overlay text)

**Visual:**
- Can add text overlay: "github.com/Biliebed/memetide"
- Or: "Live Demo: [your-url].railway.app"

**Timing:** 5 seconds

---

## 🎥 Recording Checklist

### Before Recording

- [ ] Server running: `cd ~/memetide && ./start_server.sh`
- [ ] Browser open: http://localhost:8000
- [ ] Clear browser cache (Ctrl+Shift+Del)
- [ ] Close unnecessary tabs
- [ ] Hide bookmarks bar (Ctrl+Shift+B)
- [ ] Set zoom to 100%
- [ ] Disable notifications
- [ ] Test scan once (clear results)
- [ ] Prepare second monitor for script (optional)

### During Recording

- [ ] Speak clearly and at moderate pace
- [ ] Follow script timing
- [ ] Use smooth mouse movements
- [ ] Pause briefly between sections
- [ ] Show confidence in delivery

### After Recording

- [ ] Trim start/end if needed
- [ ] Add text overlays (optional)
- [ ] Add background music (optional)
- [ ] Export as MP4 (1080p, H.264)
- [ ] Upload to YouTube

---

## 🎨 Visual Enhancements (Optional)

### Text Overlays

Add these at key moments:

**0-5s:** "MemeTide - AI Memecoin Predictor"  
**20s:** "Real-time Sentiment Analysis"  
**35s:** "On-Chain Metrics from DexScreener"  
**55s:** "Dark Mode + Export + History"  
**85s:** "github.com/Biliebed/memetide"  

### Background Music

**Free Sources:**
- YouTube Audio Library
- Uppbeat (free tier)
- Pixabay Music

**Style:** Upbeat, tech, modern (low volume, don't overpower voice)

### Transitions

Keep it simple:
- Fade in at start
- Fade out at end
- No fancy transitions (distracting)

---

## 🎤 Voiceover Tips

### If Recording Voice:

**Good Microphone Setup:**
- Use headset or USB mic
- Record in quiet room
- Speak ~1 foot from mic
- Test audio levels first

**Script Delivery:**
- Read naturally (not robotic)
- Emphasize key words: "AI", "trending", "scams", "free"
- Pause at commas
- Smile while speaking (sounds better!)

### If No Voice:

**Alternative: Text + Music**
- Add text overlays for key points
- Use upbeat background music
- Show features clearly on screen
- Let visuals speak for themselves

---

## 📤 Upload to YouTube

### Step 1: Export Video

**Filename:** `memetide-demo-okx-hackathon.mp4`

**Settings:**
- Resolution: 1920x1080
- Frame rate: 30fps
- Codec: H.264
- Bitrate: 8-10 Mbps

### Step 2: Upload

**Title:** "MemeTide - AI Memecoin Trend Predictor | OKX.AI Genesis Hackathon"

**Description:**
```
MemeTide is an AI-powered memecoin trend predictor that helps traders 
catch trending tokens early while avoiding scams.

🌊 Features:
- Real-time Twitter sentiment analysis
- On-chain metrics (price, liquidity, market cap)
- Risk scoring & scam detection
- Dark mode interface
- Export to JSON
- Scan history

🛠️ Tech Stack:
- FastAPI + Python
- DexScreener API
- TextBlob sentiment analysis
- 100% free to deploy

🔗 Links:
GitHub: https://github.com/Biliebed/memetide
Live Demo: [your-url-here]

Built for OKX.AI Genesis Hackathon 2026
Categories: Finance Copilot + Social Buzz

#OKXHackathon #Memecoin #AI #Crypto #Trading
```

**Tags:**
```
okx hackathon, memecoin, crypto trading, sentiment analysis, 
ai predictor, blockchain, defi, trading bot, crypto tools
```

**Thumbnail (Optional):**
- Screenshot of dashboard with results
- Add text: "MemeTide" + "OKX.AI Hackathon"
- Use high contrast colors

**Visibility:**
- Public (recommended for hackathon)
- Or Unlisted (only people with link)

### Step 3: Get Link

After upload, copy URL:
- Format: `https://youtu.be/VIDEO_ID`
- Use this for hackathon submission

---

## 🚀 Quick Recording Process

### 5-Minute Quick Record:

```bash
# 1. Start server
cd ~/memetide
./start_server.sh

# 2. Open browser
firefox http://localhost:8000 &

# 3. Start OBS/Loom
# Record screen + voice

# 4. Follow script:
#    - Intro (15s)
#    - Run scan (20s)
#    - Show details (20s)
#    - Features (15s)
#    - Tech (15s)
#    - Outro (5s)

# 5. Stop recording

# 6. Export MP4

# 7. Upload to YouTube
```

---

## 📊 Demo Flow Visualization

```
[0s] ──────────> Landing Page
                  ↓
[15s] ─────────> Click Scan → Loading
                  ↓
[20s] ─────────> Results Appear
                  ↓
[35s] ─────────> Scroll Details
                  ├─ On-chain metrics
                  ├─ Sample tweets
                  └─ Risk level
                  ↓
[55s] ─────────> Features Demo
                  ├─ Dark mode toggle
                  ├─ Export JSON
                  └─ History view
                  ↓
[70s] ─────────> API Docs
                  ↓
[85s] ─────────> Final Screen + GitHub
                  ↓
[90s] ──────────> END
```

---

## 🎯 Success Criteria

✅ Under 90 seconds  
✅ Shows all key features  
✅ Clear audio (if voiceover)  
✅ Smooth screen recording  
✅ Professional look  
✅ GitHub link visible  
✅ Explains value proposition  

---

## 🆘 Troubleshooting

### Screen Recording Issues

**Problem:** Lag or stuttering
- Close background apps
- Lower recording quality
- Use hardware encoding

**Problem:** No audio
- Check OBS audio sources
- Test before full recording

### Browser Issues

**Problem:** Dashboard not loading
```bash
# Restart server
cd ~/memetide
pkill -f "python api_server.py"
./start_server.sh
```

**Problem:** Results not showing
- Use mock data (default)
- Check browser console (F12)

### Video Quality

**Problem:** Blurry video
- Record at 1080p minimum
- Use 30fps (not 60fps for demo)
- Check export settings

---

## 📝 Alternative: No-Voice Demo

If you don't want to record voice:

**1. Add Text Cards**
```
[Card 1: 5s]
MemeTide
AI Memecoin Trend Predictor
─────────────────
[Card 2: Show dashboard]

[Card 3: 15s]
Scans Twitter Sentiment
+ On-Chain Metrics
─────────────────
[Show scan running]

[Card 4: 20s]
Price • Liquidity • Risk
─────────────────
[Show results]

[Card 5: 15s]
Dark Mode • Export • History
─────────────────
[Show features]

[Card 6: 10s]
Built with FastAPI
100% Free Deploy
─────────────────
[Show API docs]

[Card 7: 5s]
github.com/Biliebed/memetide
OKX.AI Genesis Hackathon
─────────────────
```

**2. Add Background Music**
- Upbeat, tech-style
- 60-70% volume
- Fade in/out

---

## ✅ Ready to Record!

**Estimated Time:** 30-60 minutes total
- Setup: 10 min
- Recording: 10-20 min (may need 2-3 takes)
- Editing: 10-20 min
- Upload: 5-10 min

**Tools Installed:**
```bash
# Check what you have
which obs-studio  # OBS
which ffmpeg      # FFmpeg
# Or use Loom (browser-based)
```

**Server Ready:**
```bash
cd ~/memetide
./start_server.sh

# Open: http://localhost:8000
```

---

**Good luck bro! Lu pasti bisa! 🎬🚀**
