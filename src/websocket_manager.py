#!/usr/bin/env python3
"""
WebSocket Manager for Real-time Alerts

Manages WebSocket connections and broadcasts alerts when high-confidence
tokens are detected.
"""

import json
import asyncio
from typing import Set, Dict, Any
from datetime import datetime
from fastapi import WebSocket


class ConnectionManager:
    """Manages WebSocket connections and broadcasts"""
    
    def __init__(self):
        # Active connections
        self.active_connections: Set[WebSocket] = set()
        
        # Connection metadata
        self.connection_metadata: Dict[WebSocket, Dict[str, Any]] = {}
        
        # Subscription filters: websocket -> set of token symbols
        self.subscriptions: Dict[WebSocket, Set[str]] = {}
        
        # Alert stats
        self.total_alerts_sent = 0
        self.total_connections = 0
    
    async def connect(self, websocket: WebSocket, client_id: str = ""):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        self.total_connections += 1
        
        # Store metadata
        self.connection_metadata[websocket] = {
            "client_id": client_id or f"client_{self.total_connections}",
            "connected_at": datetime.utcnow().isoformat(),
            "alerts_received": 0
        }
        
        # Send welcome message
        await self.send_personal_message({
            "type": "connection",
            "status": "connected",
            "client_id": self.connection_metadata[websocket]["client_id"],
            "message": "Connected to MemeTide real-time alerts",
            "timestamp": datetime.utcnow().isoformat()
        }, websocket)
        
        print(f"✅ WebSocket connected: {self.connection_metadata[websocket]['client_id']} (Total: {len(self.active_connections)})")
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            client_id = self.connection_metadata.get(websocket, {}).get("client_id", "unknown")
            self.active_connections.remove(websocket)
            
            if websocket in self.connection_metadata:
                del self.connection_metadata[websocket]
            
            if websocket in self.subscriptions:
                del self.subscriptions[websocket]
            
            print(f"❌ WebSocket disconnected: {client_id} (Total: {len(self.active_connections)})")
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Send message to specific client"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"⚠️  Failed to send message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients"""
        if not self.active_connections:
            return
        
        # Add broadcast metadata
        message["broadcast_at"] = datetime.utcnow().isoformat()
        
        # Track alert
        self.total_alerts_sent += 1
        
        # Filter recipients based on subscriptions
        recipients = []
        token_symbol = None
        
        # Extract token symbol if this is a token alert
        if message.get("type") == "token_alert":
            token_symbol = message.get("token", {}).get("symbol")
        
        for connection in self.active_connections:
            # Check subscription filter
            if token_symbol and not self.is_subscribed(connection, token_symbol):
                continue
            recipients.append(connection)
        
        message["recipients"] = len(recipients)
        
        if not recipients:
            print(f"📢 No subscribed clients for this alert")
            return
        
        print(f"📢 Broadcasting alert to {len(recipients)} client(s)...")
        
        # Send to subscribed connections
        disconnected = set()
        for connection in recipients:
            try:
                await connection.send_json(message)
                
                # Update connection stats
                if connection in self.connection_metadata:
                    self.connection_metadata[connection]["alerts_received"] += 1
            except Exception as e:
                print(f"⚠️  Failed to broadcast to client: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
    
    def subscribe(self, websocket: WebSocket, tokens: Set[str]):
        """Subscribe client to specific tokens"""
        self.subscriptions[websocket] = {t.upper() for t in tokens}
        print(f"📝 Client subscribed to: {', '.join(self.subscriptions[websocket])}")
    
    def unsubscribe(self, websocket: WebSocket):
        """Unsubscribe client from all filters (subscribe to all)"""
        if websocket in self.subscriptions:
            del self.subscriptions[websocket]
            print(f"📝 Client unsubscribed (now receives all alerts)")
    
    def is_subscribed(self, websocket: WebSocket, token_symbol: str) -> bool:
        """Check if client is subscribed to token"""
        # No filter = subscribed to everything
        if websocket not in self.subscriptions:
            return True
        
        # Check if token in filter
        return token_symbol.upper() in self.subscriptions[websocket]
    
    async def broadcast_token_alert(self, token_data: Dict[str, Any], scan_id: str):
        """
        Broadcast high-confidence token alert
        
        Args:
            token_data: Token prediction data
            scan_id: Scan ID for reference
        """
        # Extract sentiment safely (could be object or dict)
        sentiment = token_data.get("sentiment", {})
        if hasattr(sentiment, "__dict__"):
            sentiment_compound = getattr(sentiment, "compound", 0)
        elif isinstance(sentiment, dict):
            sentiment_compound = sentiment.get("compound", 0)
        else:
            sentiment_compound = 0
        
        # Extract metrics safely
        metrics = token_data.get("metrics", {})
        if hasattr(metrics, "__dict__"):
            metrics = metrics.__dict__
        
        alert = {
            "type": "token_alert",
            "scan_id": scan_id,
            "token": {
                "symbol": token_data.get("token_symbol"),
                "score": token_data.get("score"),
                "confidence": token_data.get("confidence"),
                "risk_level": token_data.get("risk_level"),
                "mentions": token_data.get("mention_count"),
                "sentiment": sentiment_compound,
                "contract": metrics.get("contract_address") if isinstance(metrics, dict) else None,
                "price_usd": metrics.get("price_usd") if isinstance(metrics, dict) else None,
                "market_cap": metrics.get("market_cap") if isinstance(metrics, dict) else None,
            },
            "message": self._generate_alert_message(token_data),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.broadcast(alert)
    
    def _generate_alert_message(self, token_data: Dict[str, Any]) -> str:
        """Generate human-readable alert message"""
        symbol = token_data.get("token_symbol")
        confidence = token_data.get("confidence")
        score = token_data.get("score")
        
        # Extract sentiment safely
        sentiment = token_data.get("sentiment", {})
        if hasattr(sentiment, "compound"):
            sentiment_value = sentiment.compound
        elif isinstance(sentiment, dict):
            sentiment_value = sentiment.get("compound", 0)
        else:
            sentiment_value = 0
        
        if confidence == "high":
            return f"🔥 HIGH confidence: ${symbol} detected (Score: {score:.1f}, Sentiment: {sentiment_value:.2f})"
        elif confidence == "medium":
            return f"⚠️ MEDIUM confidence: ${symbol} trending (Score: {score:.1f}, Sentiment: {sentiment_value:.2f})"
        else:
            return f"ℹ️ LOW confidence: ${symbol} detected (Score: {score:.1f}, Sentiment: {sentiment_value:.2f})"
    
    async def broadcast_scan_complete(self, scan_result: Dict[str, Any]):
        """Broadcast scan completion notification"""
        message = {
            "type": "scan_complete",
            "scan_id": scan_result.get("scan_id"),
            "tokens_found": scan_result.get("unique_tokens"),
            "duration": scan_result.get("duration_seconds"),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.broadcast(message)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get WebSocket manager statistics"""
        return {
            "active_connections": len(self.active_connections),
            "total_connections": self.total_connections,
            "total_alerts_sent": self.total_alerts_sent,
            "clients": [
                {
                    "client_id": meta.get("client_id"),
                    "connected_at": meta.get("connected_at"),
                    "alerts_received": meta.get("alerts_received", 0)
                }
                for meta in self.connection_metadata.values()
            ]
        }


# Global connection manager instance
manager = ConnectionManager()
