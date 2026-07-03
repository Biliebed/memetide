#!/usr/bin/env python3
"""
Test WebSocket alerts locally or on production
"""

import asyncio
import websockets
import json
import sys
from datetime import datetime

# Default to production URL
WS_URL = "wss://memetide-production.up.railway.app/ws/alerts?client_id=test_client"

# Override with local if specified
if len(sys.argv) > 1 and sys.argv[1] == "local":
    WS_URL = "ws://localhost:8000/ws/alerts?client_id=test_client"

print(f"🌊 MemeTide WebSocket Test")
print(f"   Connecting to: {WS_URL}\n")

async def listen_alerts():
    """Connect to WebSocket and listen for alerts"""
    try:
        async with websockets.connect(WS_URL) as ws:
            print(f"✅ Connected at {datetime.now().strftime('%H:%M:%S')}\n")
            
            # Listen for messages
            async for message in ws:
                data = json.loads(message)
                handle_message(data)
                
    except websockets.exceptions.WebSocketException as e:
        print(f"❌ WebSocket error: {e}")
    except KeyboardInterrupt:
        print("\n\n👋 Disconnected by user")
    except Exception as e:
        print(f"❌ Error: {e}")

def handle_message(data):
    """Handle incoming WebSocket message"""
    msg_type = data.get("type")
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    if msg_type == "connection":
        print(f"[{timestamp}] 🔗 {data.get('message')}")
        print(f"           Client ID: {data.get('client_id')}\n")
    
    elif msg_type == "token_alert":
        token = data.get("token", {})
        symbol = token.get("symbol")
        confidence = token.get("confidence", "").upper()
        score = token.get("score", 0)
        mentions = token.get("mentions", 0)
        sentiment = token.get("sentiment", 0)
        risk = token.get("risk_level", "unknown")
        
        # Emoji based on confidence
        emoji = "🔥" if confidence == "HIGH" else "⚠️" if confidence == "MEDIUM" else "ℹ️"
        
        print(f"[{timestamp}] {emoji} ALERT: ${symbol}")
        print(f"           Confidence: {confidence}")
        print(f"           Score: {score:.1f}")
        print(f"           Mentions: {mentions}")
        print(f"           Sentiment: {sentiment:.2f}")
        print(f"           Risk: {risk}")
        
        if token.get("price_usd"):
            print(f"           Price: ${token['price_usd']:.2e}")
        if token.get("market_cap"):
            print(f"           Market Cap: ${token['market_cap']:,.0f}")
        
        print()
    
    elif msg_type == "scan_complete":
        print(f"[{timestamp}] ✅ Scan complete")
        print(f"           Scan ID: {data.get('scan_id')}")
        print(f"           Tokens found: {data.get('tokens_found')}")
        print(f"           Duration: {data.get('duration'):.2f}s\n")
    
    elif msg_type == "pong":
        print(f"[{timestamp}] 🏓 Pong received\n")
    
    else:
        print(f"[{timestamp}] 📨 {msg_type}: {json.dumps(data, indent=2)}\n")

if __name__ == "__main__":
    print("💡 Tip: Open another terminal and run a scan to see alerts:")
    print("   curl -X POST https://memetide-production.up.railway.app/scan \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"min_mentions\": 3, \"use_mock_data\": true}'\n")
    print("=" * 60)
    print()
    
    try:
        asyncio.run(listen_alerts())
    except KeyboardInterrupt:
        print("\n\n👋 Disconnected")
