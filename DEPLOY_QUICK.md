# 🚀 Deploy MemeTide in 5 Minutes

Quick deploy to Railway (easiest option).

---

## Step 1: Push to GitHub (2 min)

```bash
cd ~/memetide

# If repo doesn't exist on GitHub:
# 1. Go to https://github.com/new
# 2. Name: memetide
# 3. Create (don't add README/license)

# Add remote and push
git remote add origin https://github.com/Biliebed/memetide.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy to Railway (3 min)

1. **Go to Railway:** https://railway.app

2. **Sign up/Login** (GitHub account recommended)

3. **New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub
   - Choose `Biliebed/memetide`

4. **Wait for deploy** (~2 minutes)
   - Railway auto-detects Python
   - Installs dependencies from requirements.txt
   - Runs `uvicorn api_server:app`

5. **Get your URL:**
   - Click on your deployment
   - Go to "Settings" → "Domains"
   - Copy the generated URL (e.g., `memetide-production.up.railway.app`)

---

## Step 3: Test Live API (30 sec)

```bash
# Replace with your Railway URL
export API_URL="https://memetide-production.up.railway.app"

# Health check
curl $API_URL/health

# Run scan
curl -X POST $API_URL/scan \
  -H "Content-Type: application/json" \
  -d '{"min_mentions": 3, "use_mock_data": true, "top_n": 3}'

# Interactive docs
open $API_URL/docs
```

---

## ✅ Done!

Your API is live at: `https://memetide-production.up.railway.app`

**Next steps:**
- Update README.md with live demo link
- Test all endpoints in Swagger UI (`/docs`)
- Submit to OKX.AI with production URL
- Add custom domain (optional)

---

## Alternative: Render (if Railway doesn't work)

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect GitHub repo `Biliebed/memetide`
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn api_server:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"
6. Wait ~5 minutes
7. Get URL from dashboard

---

## Troubleshooting

**Build failed?**
- Check Railway logs for error
- Ensure `requirements.txt` is committed
- Python version: 3.11+ required

**Can't connect?**
- Railway URL takes ~30s after deploy
- Check "Deployments" tab for status
- Ensure health check passes: `/health`

**Need help?**
- Railway docs: https://docs.railway.app
- MemeTide issues: https://github.com/Biliebed/memetide/issues

---

**Total time: ~5 minutes** ⏱️

**Cost: FREE** (Railway 500 hrs/month) 💰

**Built for OKX.AI Genesis Hackathon 2026** 🚀
