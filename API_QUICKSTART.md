# MemeTide API - Quick Start

Get the API server running in 2 minutes.

---

## Prerequisites

- Python 3.10+
- Dependencies installed (`pip install -r requirements.txt`)

---

## Start Server

**Easy way:**
```bash
cd ~/memetide
./start_server.sh
```

**Manual way:**
```bash
cd ~/memetide
source venv/bin/activate
python api_server.py
```

Server will start at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Test Endpoints

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

**View History:**
```bash
curl http://localhost:8000/history?limit=5
```

**Get Stats:**
```bash
curl http://localhost:8000/stats
```

---

## Automated Tests

```bash
cd ~/memetide
source venv/bin/activate
python test_api.py
```

Expected output:
```
============================================================
🌊 MEMETIDE API TEST
============================================================

[1/7] Testing root endpoint...
✅ Root: MemeTide API v1.0.0

[2/7] Testing health check...
✅ Health: healthy, uptime 25.3s

[3/7] Testing scan endpoint (mock data)...
✅ Scan complete:
   - Scan ID: 9568f3c1
   - Duration: 0.00s
   - Tokens found: 3

...

============================================================
✅ API TESTS COMPLETE
============================================================
```

---

## API Documentation

Full endpoint reference: [API.md](API.md)

Or browse interactive docs: http://localhost:8000/docs

---

## Production Deployment

**With Gunicorn:**
```bash
gunicorn api_server:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

**With Docker:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Troubleshooting

**Port already in use:**
```bash
lsof -i :8000
kill -9 <PID>
```

**Dependencies missing:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Server won't start:**
```bash
# Check Python version
python --version  # Need 3.10+

# Reinstall FastAPI
pip install --force-reinstall fastapi uvicorn
```

---

**Built for OKX.AI Genesis Hackathon 2026** 🚀
