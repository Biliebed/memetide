# 🎬 Demo Video Checklist

Quick checklist for recording demo video.

---

## ✅ Pre-Recording (5 minutes)

### Server Setup
- [ ] `cd ~/memetide && ./start_server.sh`
- [ ] Wait for "Uvicorn running on http://0.0.0.0:8000"
- [ ] Test: Open http://localhost:8000 in browser
- [ ] Test scan once (to warm up)
- [ ] Clear scan results

### Browser Setup
- [ ] Open clean browser tab
- [ ] Navigate to http://localhost:8000
- [ ] Set zoom to 100% (Ctrl+0)
- [ ] Hide bookmarks bar (Ctrl+Shift+B)
- [ ] Clear any notifications
- [ ] Close other tabs (optional but cleaner)

### Recording Tool
- [ ] OBS Studio running (or Loom, or FFmpeg ready)
- [ ] Set recording area (1920x1080 recommended)
- [ ] Test audio levels (if recording voice)
- [ ] Set output format: MP4, H.264

### Script
- [ ] Open `demo_script.txt` on second monitor
- [ ] Or print it out
- [ ] Practice once (optional)

---

## 🎥 Recording (10-20 minutes)

### Take 1
- [ ] Click Record
- [ ] Wait 3 seconds
- [ ] Start speaking/showing
- [ ] Follow script timing
- [ ] Stop recording after 90 seconds

### Review
- [ ] Play back recording
- [ ] Check audio quality (if applicable)
- [ ] Check visual clarity
- [ ] Check timing (under 90s?)

### Take 2+ (if needed)
- [ ] Reset browser (refresh to landing page)
- [ ] Re-record if needed
- [ ] Keep best take

---

## ✂️ Post-Production (10-20 minutes)

### Editing (Optional)
- [ ] Trim start (first 1-2 seconds if needed)
- [ ] Trim end (after "thank you")
- [ ] Add text overlay: "github.com/Biliebed/memetide" (optional)
- [ ] Add fade in/out (optional)
- [ ] Add background music (optional, low volume)

### Export
- [ ] Export as MP4
- [ ] Resolution: 1920x1080 (or 1280x720 minimum)
- [ ] Frame rate: 30fps
- [ ] Codec: H.264
- [ ] Bitrate: 8-10 Mbps (high quality)
- [ ] File size: <100MB (target)

---

## 📤 Upload to YouTube (5-10 minutes)

### Video Details
- [ ] **Title:** "MemeTide - AI Memecoin Trend Predictor | OKX.AI Genesis Hackathon"
- [ ] **Description:** Copy from DEMO_VIDEO_GUIDE.md
- [ ] **Tags:** okx hackathon, memecoin, crypto, ai, trading
- [ ] **Visibility:** Public (or Unlisted)
- [ ] **Category:** Science & Technology

### After Upload
- [ ] Copy YouTube URL: `https://youtu.be/VIDEO_ID`
- [ ] Test video plays correctly
- [ ] Check audio/video quality

---

## 📝 Update Project

### Add Video Link
```bash
cd ~/memetide

# Edit README.md
nano README.md

# Add at top:
## 🎬 Demo Video

**Watch:** https://youtu.be/YOUR_VIDEO_ID

# Save and commit
git add README.md
git commit -m "Add demo video link"
git push
```

---

## 🚀 Hackathon Submission

### Prepare Submission Form
- [ ] Project name: **MemeTide**
- [ ] Tagline: **AI-powered memecoin trend predictor**
- [ ] Video URL: `https://youtu.be/YOUR_VIDEO_ID`
- [ ] GitHub: `https://github.com/Biliebed/memetide`
- [ ] Live demo: `https://your-app.railway.app` (if deployed)
- [ ] Categories: **Finance Copilot + Social Buzz**

### Submission Checklist
- [ ] Video uploaded and public
- [ ] GitHub repo public
- [ ] README complete with demo link
- [ ] Live deployment (optional but recommended)
- [ ] All links working

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Setup | 5 min |
| Recording (2-3 takes) | 10-20 min |
| Editing | 10-20 min |
| Upload | 5-10 min |
| Update project | 5 min |
| **Total** | **35-60 min** |

---

## 🆘 Quick Fixes

### Server not running?
```bash
cd ~/memetide
pkill -f "python api_server.py"
./start_server.sh
```

### Browser issues?
```bash
# Clear cache: Ctrl+Shift+Del
# Or use private/incognito window
firefox --private-window http://localhost:8000
```

### Scan not working?
- Use mock data (default setting)
- Check browser console: F12

### Recording laggy?
- Close background apps
- Lower recording resolution to 720p
- Use hardware encoding in OBS

---

## ✅ Done!

When complete, you should have:
- ✅ 90-second demo video
- ✅ YouTube link
- ✅ README updated
- ✅ Ready for hackathon submission

---

**Good luck! 🎬🚀**
