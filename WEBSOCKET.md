# 📡 WebSocket Real-time Alerts

MemeTide v1.1+ includes WebSocket support for real-time push notifications when high-confidence tokens are detected.

---

## Quick Start

### Web Client (Recommended)

**Open the live demo:**
```
https://memetide-production.up.railway.app/static/alerts.html
```

1. Click "Connect to Alerts"
2. Run a scan from another tab: https://memetide-production.up.railway.app/docs
3. Execute `/scan` endpoint
4. Watch alerts appear in real-time ⚡

---

## Connection

**WebSocket URL:**
```
wss://memetide-production.up.railway.app/ws/alerts
```

**Query Parameters:**
- `client_id` (optional): Client identifier for tracking

**Example:**
```
wss://memetide-production.up.railway.app/ws/alerts?client_id=my_app
```

---

## Message Types

### 1. Connection Confirmation

Sent immediately after connection:

```json
{
  "type": "connection",
  "status": "connected",
  "client_id": "client_1",
  "message": "Connected to MemeTide real-time alerts",
  "timestamp": "2026-07-03T18:00:00.000000"
}
```

---

### 2. Token Alert

Sent when high/medium confidence token detected:

```json
{
  "type": "token_alert",
  "scan_id": "abc123",
  "token": {
    "symbol": "FLOKI",
    "score": 57.2,
    "confidence": "medium",
    "risk_level": "very_low",
    "mentions": 11,
    "sentiment": 0.74,
    "contract": "0xfb5B838b6cfEEdC2873aB27866079AC55363D37E",
    "price_usd": 2.302e-05,
    "market_cap": 94498436.0
  },
  "message": "⚠️ MEDIUM confidence: $FLOKI trending (Score: 57.2, Sentiment: 0.74)",
  "timestamp": "2026-07-03T18:05:30.000000",
  "broadcast_at": "2026-07-03T18:05:30.100000",
  "recipients": 3
}
```

**Alert Rules:**
- Only HIGH and MEDIUM confidence tokens trigger alerts
- Top 3 tokens per scan (ranked by score)
- Sent immediately after scan completion

---

### 3. Scan Complete

Sent after scan finishes:

```json
{
  "type": "scan_complete",
  "scan_id": "abc123",
  "tokens_found": 5,
  "duration": 0.71,
  "timestamp": "2026-07-03T18:05:31.000000",
  "broadcast_at": "2026-07-03T18:05:31.200000",
  "recipients": 3
}
```

---

## Client Commands

Send commands to the server:

### Ping/Pong

Keep connection alive:

```
→ ping
← {"type": "pong", "timestamp": "2026-07-03T18:00:00"}
```

### Request Stats

Get WebSocket statistics:

```json
→ {"command": "stats"}
← {
    "type": "stats",
    "data": {
      "active_connections": 5,
      "total_connections": 42,
      "total_alerts_sent": 128,
      "clients": [
        {
          "client_id": "web_1234",
          "connected_at": "2026-07-03T17:50:00",
          "alerts_received": 15
        }
      ]
    }
  }
```

---

## Client Examples

### JavaScript (Browser)

```javascript
const ws = new WebSocket('wss://memetide-production.up.railway.app/ws/alerts?client_id=my_app');

ws.onopen = () => {
  console.log('Connected to MemeTide alerts');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'token_alert') {
    console.log(`🔥 Alert: $${data.token.symbol} - ${data.token.confidence}`);
    console.log(`   Score: ${data.token.score}`);
    console.log(`   Risk: ${data.token.risk_level}`);
  }
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected from MemeTide alerts');
};

// Send ping every 30s
setInterval(() => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send('ping');
  }
}, 30000);
```

---

### Python

```python
import asyncio
import websockets
import json

async def listen_alerts():
    uri = "wss://memetide-production.up.railway.app/ws/alerts?client_id=python_client"
    
    async with websockets.connect(uri) as ws:
        print("Connected to MemeTide alerts")
        
        async for message in ws:
            data = json.loads(message)
            
            if data['type'] == 'token_alert':
                token = data['token']
                print(f"🔥 Alert: ${token['symbol']}")
                print(f"   Confidence: {token['confidence']}")
                print(f"   Score: {token['score']}")
                print(f"   Mentions: {token['mentions']}")
                print()

if __name__ == "__main__":
    asyncio.run(listen_alerts())
```

**Run:**
```bash
pip install websockets
python listen_alerts.py
```

---

### Node.js

```javascript
const WebSocket = require('ws');

const ws = new WebSocket('wss://memetide-production.up.railway.app/ws/alerts?client_id=node_client');

ws.on('open', () => {
  console.log('Connected to MemeTide alerts');
});

ws.on('message', (data) => {
  const message = JSON.parse(data);
  
  if (message.type === 'token_alert') {
    const { symbol, confidence, score } = message.token;
    console.log(`🔥 Alert: $${symbol} - ${confidence} (${score})`);
  }
});

ws.on('close', () => {
  console.log('Disconnected from MemeTide alerts');
});

// Ping every 30s
setInterval(() => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send('ping');
  }
}, 30000);
```

**Run:**
```bash
npm install ws
node listen_alerts.js
```

---

### cURL (Testing Only)

Test connection (limited, doesn't support persistent connection):

```bash
curl -i -N -H "Connection: Upgrade" \
     -H "Upgrade: websocket" \
     -H "Sec-WebSocket-Version: 13" \
     -H "Sec-WebSocket-Key: $(echo -n 'test' | base64)" \
     https://memetide-production.up.railway.app/ws/alerts
```

---

## REST API for WebSocket Stats

Get current WebSocket statistics without connecting:

```bash
curl https://memetide-production.up.railway.app/ws/stats
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "active_connections": 5,
    "total_connections": 42,
    "total_alerts_sent": 128,
    "clients": [...]
  }
}
```

---

## Use Cases

### 1. Trading Bot

Connect to WebSocket → receive high-confidence alerts → auto-execute trades

```python
async def trading_bot():
    async with websockets.connect(ws_url) as ws:
        async for message in ws:
            data = json.loads(message)
            if data['type'] == 'token_alert' and data['token']['confidence'] == 'high':
                execute_trade(data['token'])
```

---

### 2. Notification Service

Forward alerts to Telegram/Discord/Slack:

```python
async def notification_service():
    async with websockets.connect(ws_url) as ws:
        async for message in ws:
            data = json.loads(message)
            if data['type'] == 'token_alert':
                send_telegram_message(format_alert(data))
```

---

### 3. Dashboard

Real-time dashboard with live updates (see `static/alerts.html`)

---

### 4. Research Tool

Log all alerts for backtesting:

```python
async def logger():
    async with websockets.connect(ws_url) as ws:
        async for message in ws:
            data = json.loads(message)
            if data['type'] == 'token_alert':
                save_to_database(data)
```

---

## Connection Management

### Heartbeat

Send `ping` every 30 seconds to keep connection alive:

```javascript
setInterval(() => ws.send('ping'), 30000);
```

### Reconnection

Handle disconnections gracefully:

```javascript
function connect() {
  const ws = new WebSocket(wsUrl);
  
  ws.onclose = () => {
    console.log('Disconnected. Reconnecting in 5s...');
    setTimeout(connect, 5000);
  };
  
  // ... other handlers
}

connect();
```

---

## Rate Limits & Best Practices

**No rate limits on WebSocket connections** (for now)

**Best Practices:**
1. **One connection per client** - Don't open multiple connections from same app
2. **Heartbeat** - Send ping every 30s to detect disconnections
3. **Reconnect on close** - Auto-reconnect with exponential backoff
4. **Handle errors** - WebSocket can disconnect anytime
5. **Filter client-side** - Subscribe to all, filter locally

---

## Troubleshooting

### Connection refused
- Check URL (wss:// for HTTPS, ws:// for HTTP)
- Verify server is running: `curl https://memetide-production.up.railway.app/health`

### No alerts received
- Run a scan manually: `POST /scan` with mock data
- Check WebSocket stats: `GET /ws/stats`
- Verify connection: send `{"command": "stats"}`

### Connection drops
- Server restarts (Railway auto-restarts)
- Network issues
- Implement auto-reconnect

---

## Next Features (v1.2+)

- [ ] **Subscription filters** - Subscribe to specific tokens only
- [ ] **Authentication** - JWT-based WebSocket auth
- [ ] **Private channels** - Per-user private alert streams
- [ ] **Rate limiting** - Throttle alerts per client
- [ ] **Message persistence** - Replay missed alerts on reconnect

---

## Architecture

```
Scan Engine (api_server.py)
        ↓
  Detect high/medium token
        ↓
WebSocket Manager (websocket_manager.py)
        ↓
  Broadcast to all clients
        ↓
   [Client 1] [Client 2] [Client 3]
```

**Components:**
- `api_server.py` - WebSocket endpoint `/ws/alerts`
- `websocket_manager.py` - Connection manager & broadcaster
- Integration in `/scan` endpoint - Auto-broadcast on detection

---

## Live Demo

**Web UI:** https://memetide-production.up.railway.app/static/alerts.html

**Steps:**
1. Open alerts page
2. Click "Connect to Alerts"
3. Open another tab: https://memetide-production.up.railway.app/docs
4. Execute `POST /scan` with mock data
5. Watch alerts appear in real-time 🚀

---

**Built for OKX.AI Genesis Hackathon 2026** 🌊
