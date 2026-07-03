# 🔧 Railway Deployment Troubleshooting

Common issues and fixes for Railway deployment.

---

## ✅ Fixes Applied

Recent fixes pushed to GitHub:

1. **NLTK Data Issue** - Added start.sh script to download NLTK data
2. **Procfile Updated** - Changed to use start script
3. **NLTK Package** - Added to requirements.txt
4. **Build Optimization** - Added .railwayignore

---

## 🚀 Deploy Steps (After Fixes)

### Option 1: Redeploy Existing Project

If you already created Railway project:

1. Go to your Railway project
2. Click **"Deployments"** tab
3. Click **"Redeploy"** button (force new build)
4. Or click **"Deploy"** → **"Trigger Deploy"**
5. Watch logs for errors

### Option 2: Fresh Deploy

If you want to start fresh:

1. Delete old project (if exists)
2. **New Project** → **Deploy from GitHub**
3. Select **Biliebed/memetide**
4. Railway auto-deploys with fixes

---

## 📋 Common Errors & Fixes

### Error 1: "ModuleNotFoundError: No module named 'nltk'"

**Cause:** NLTK not in requirements.txt

**Fix:** ✅ Already fixed - nltk added to requirements.txt

---

### Error 2: "Resource punkt not found"

**Cause:** NLTK data not downloaded

**Fix:** ✅ Already fixed - start.sh downloads NLTK data

---

### Error 3: "Address already in use" or Port binding

**Cause:** App not listening on $PORT

**Fix:** ✅ Already fixed - start.sh uses ${PORT:-8000}

---

### Error 4: "Static files not found"

**Cause:** static/ directory not included

**Fix:** 
- ✅ Static files exist in repo
- ✅ .railwayignore doesn't exclude static/
- Check: Settings → Environment → Add `STATIC_ROOT=/app/static` (if needed)

---

### Error 5: Build timeout or too slow

**Cause:** Installing too many dependencies

**Fix:**
- ✅ .railwayignore excludes venv/ and test files
- Railway caches dependencies after first build
- Subsequent builds ~30-60 seconds

---

### Error 6: "Application failed to respond"

**Cause:** App crashed on startup

**Fix:** Check logs for actual error:
1. Railway Dashboard → Your Project
2. Click **"Deployments"**
3. Click latest deployment
4. View **"Build Logs"** and **"Deploy Logs"**
5. Look for Python traceback

Common causes:
- Missing environment variables
- Import errors
- Database connection (N/A for MemeTide)

---

## 🔍 How to Check Logs

### Build Logs (During pip install)

```
Deployments → Latest → Build Logs
```

Look for:
- `Successfully installed ...` ✅
- `ERROR: ...` ❌
- `Command "python setup.py egg_info" failed` ❌

### Deploy Logs (During startup)

```
Deployments → Latest → Deploy Logs  
```

Look for:
- `✅ NLTK data ready` ✅
- `🚀 Starting Uvicorn...` ✅
- `Uvicorn running on ...` ✅
- `Traceback (most recent call last):` ❌

---

## ✅ Checklist for Successful Deploy

- [x] Code pushed to GitHub
- [x] requirements.txt includes all packages
- [x] nltk in requirements.txt
- [x] Procfile uses start.sh
- [x] start.sh downloads NLTK data
- [x] start.sh is executable (chmod +x)
- [x] static/ directory exists with index.html
- [x] api_server.py mounts static files
- [x] PORT environment variable handled

---

## 🎯 Expected Behavior

### Successful Build (1-2 minutes)

```
#1 [build] Installing dependencies...
#2 [build] Collecting fastapi>=0.115.0
#3 [build] Collecting uvicorn>=0.30.0
...
#10 [build] Successfully installed fastapi-0.115.0 ...
#11 [build] Build complete!
```

### Successful Deploy (<30 seconds)

```
🌊 MemeTide Starting...
[nltk_data] Downloading package punkt...
[nltk_data]   Package punkt is already up-to-date!
✅ NLTK data ready
🚀 Starting Uvicorn...
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Health Check Passing

After deploy, Railway automatically checks:
```
GET https://your-app.railway.app/health
→ 200 OK {"status": "healthy", ...}
```

---

## 🌐 After Successful Deploy

### Get Your URL

1. Go to: Settings → Domains
2. Click: **"Generate Domain"**
3. Get: `https://memetide-production-XXXX.up.railway.app`

### Test Deployment

```bash
# Health check
curl https://your-app.railway.app/health

# Dashboard (should redirect)
curl -I https://your-app.railway.app/

# API scan
curl -X POST https://your-app.railway.app/scan \
  -H "Content-Type: application/json" \
  -d '{"min_mentions": 3, "use_mock_data": true}'
```

---

## 🆘 Still Having Issues?

### Copy Exact Error Message

1. Railway Dashboard → Deployments → Latest
2. Open Deploy Logs
3. Scroll to bottom
4. Copy full error traceback
5. Share with me for debugging

### Alternative: Try Render

If Railway keeps failing, try Render.com instead:

1. https://render.com → Sign up with GitHub
2. New + → Web Service
3. Connect: Biliebed/memetide
4. Build: `pip install -r requirements.txt`
5. Start: `bash start.sh`
6. Deploy!

---

## 📊 Current Status

**GitHub:** https://github.com/Biliebed/memetide ✅  
**Latest Commit:** Fix Railway deployment issues ✅  
**Files Ready:** All deployment configs included ✅  
**Expected Result:** Should deploy successfully now ✅  

---

**Try deploying again bro! Fixes udah di-push.** 🚀
