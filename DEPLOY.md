# MemeTide Deployment Guide

Deploy MemeTide API to production cloud platforms.

---

## Quick Deploy Options

| Platform | Difficulty | Free Tier | Deploy Time |
|----------|-----------|-----------|-------------|
| Railway | ⭐ Easy | 500 hrs/month | 5 min |
| Render | ⭐ Easy | 750 hrs/month | 5 min |
| Fly.io | ⭐⭐ Medium | 3 VMs free | 10 min |
| DigitalOcean | ⭐⭐⭐ Hard | $200 credit | 20 min |

**Recommended:** Railway or Render (easiest, good free tier)

---

## Option 1: Railway (Recommended)

### Prerequisites
- GitHub account
- Railway account (free): https://railway.app

### Steps

**1. Push to GitHub**
```bash
cd ~/memetide

# Initialize if not already
git init
git add .
git commit -m "Add deployment config"

# Create repo at github.com/Biliebed/memetide
git remote add origin https://github.com/Biliebed/memetide.git
git branch -M main
git push -u origin main
```

**2. Deploy to Railway**

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose `Biliebed/memetide`
5. Railway auto-detects Python and deploys

**3. Configure**

Railway auto-sets `PORT` environment variable. No extra config needed.

**4. Get URL**

Railway generates URL like: `memetide-production.up.railway.app`

**5. Test**
```bash
curl https://memetide-production.up.railway.app/health
```

### Custom Domain (Optional)

1. Go to Railway project settings
2. Click "Domains"
3. Add custom domain (e.g., api.memetide.com)
4. Update DNS CNAME record

---

## Option 2: Render

### Steps

**1. Push to GitHub** (same as Railway)

**2. Deploy to Render**

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect GitHub repo `Biliebed/memetide`
4. Configure:
   - **Name:** memetide-api
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn api_server:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"

**3. Wait for deploy** (~5 min)

**4. Get URL**

Render generates URL like: `memetide-api.onrender.com`

**5. Test**
```bash
curl https://memetide-api.onrender.com/health
```

### Notes

- Free tier sleeps after 15 min inactivity
- First request after sleep takes ~30s
- Upgrade to paid ($7/month) for always-on

---

## Option 3: Fly.io

### Prerequisites
- Fly.io account: https://fly.io
- Fly CLI installed

### Steps

**1. Install Fly CLI**
```bash
curl -L https://fly.io/install.sh | sh
```

**2. Login**
```bash
fly auth login
```

**3. Launch app**
```bash
cd ~/memetide
fly launch

# Answer prompts:
# - App name: memetide-api
# - Region: Choose closest
# - PostgreSQL: No
# - Redis: No
```

**4. Deploy**
```bash
fly deploy
```

**5. Get URL**
```bash
fly status
# URL: https://memetide-api.fly.dev
```

**6. Test**
```bash
curl https://memetide-api.fly.dev/health
```

---

## Option 4: Docker (Self-Hosted)

### Prerequisites
- Docker installed
- Server with public IP

### Steps

**1. Build image**
```bash
cd ~/memetide
docker build -t memetide-api .
```

**2. Run container**
```bash
docker run -d \
  -p 8000:8000 \
  --name memetide \
  --restart unless-stopped \
  memetide-api
```

**3. Test**
```bash
curl http://YOUR_SERVER_IP:8000/health
```

**4. Setup reverse proxy (Nginx)**
```nginx
server {
    listen 80;
    server_name api.memetide.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**5. Setup SSL (Let's Encrypt)**
```bash
sudo certbot --nginx -d api.memetide.com
```

---

## Environment Variables

Set these in your platform's dashboard:

| Variable | Value | Required |
|----------|-------|----------|
| `PORT` | 8000 | Auto-set by platform |
| `NITTER_URL` | https://nitter.net | Optional (for real Twitter) |

---

## Post-Deployment

### Test Endpoints

```bash
# Health check
curl https://your-domain.com/health

# Scan (mock data)
curl -X POST https://your-domain.com/scan \
  -H "Content-Type: application/json" \
  -d '{"min_mentions": 3, "use_mock_data": true}'

# Interactive docs
open https://your-domain.com/docs
```

### Monitor

**Railway:** Built-in logs and metrics  
**Render:** Logs tab in dashboard  
**Fly.io:** `fly logs`  
**Docker:** `docker logs memetide`

### Update

**Railway/Render:** Just push to GitHub, auto-deploys  
**Fly.io:** Run `fly deploy`  
**Docker:** Rebuild and restart container

---

## Production Checklist

Before going live:

- [ ] Enable HTTPS (auto on Railway/Render/Fly)
- [ ] Set CORS origins to your frontend domain
- [ ] Add rate limiting (see API.md)
- [ ] Set up monitoring/alerts
- [ ] Add authentication for sensitive endpoints
- [ ] Configure custom domain
- [ ] Test all endpoints
- [ ] Update OKX.AI submission with live URL

---

## Cost Estimates

**Free Tier Limits:**

| Platform | Compute | Bandwidth | Storage | Limit |
|----------|---------|-----------|---------|-------|
| Railway | 500 hrs/mo | 100 GB | 1 GB | $5 after |
| Render | 750 hrs/mo | 100 GB | 0 GB | Sleeps |
| Fly.io | 3 VMs | 160 GB | 3 GB | $0 |

**Paid Plans:**

- Railway: $5/month (500 hrs) + usage
- Render: $7/month (always-on)
- Fly.io: ~$5-10/month depending on usage

**Recommendation:** Start free, upgrade when needed.

---

## Troubleshooting

### Port Binding Error

**Error:** `[Errno 98] Address already in use`

**Fix:** Platform sets `PORT` env var, use it:
```python
port = int(os.getenv("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
```

Already fixed in `api_server.py`.

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Fix:** Ensure `requirements.txt` is committed:
```bash
git add requirements.txt
git commit -m "Add requirements"
git push
```

### Slow Cold Starts

Free tiers sleep after inactivity:
- Railway: No sleep
- Render: 15 min sleep (30s wake)
- Fly.io: No sleep

**Fix:** Upgrade to paid tier or use uptime monitor (UptimeRobot).

### NLTK Data Missing

**Error:** `Resource 'punkt' not found`

**Fix:** Already handled in `Dockerfile`:
```dockerfile
RUN python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"
```

---

## Custom Domain Setup

### Railway

1. Go to project → Settings → Domains
2. Click "Add Domain"
3. Enter your domain (e.g., api.memetide.com)
4. Add CNAME record at your DNS provider:
   - Name: `api`
   - Value: `memetide-production.up.railway.app`

### Render

1. Go to service → Settings → Custom Domain
2. Enter domain
3. Add CNAME record:
   - Name: `api`
   - Value: `memetide-api.onrender.com`

### Fly.io

1. Add domain:
   ```bash
   fly certs create api.memetide.com
   ```
2. Add A/AAAA records (shown in output)

---

## CI/CD (Auto-Deploy)

**Railway/Render:** Already enabled by default.

**GitHub Actions (for Fly.io):**

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Fly.io

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

---

## Next Steps

1. Deploy to Railway/Render (5 min)
2. Test live URL
3. Update README with live demo link
4. Submit to OKX.AI with production URL
5. Monitor logs for errors
6. Scale up if traffic increases

---

**Built for OKX.AI Genesis Hackathon 2026** 🚀
