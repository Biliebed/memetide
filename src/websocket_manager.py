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
        message["recipients"] = len(self.active_connections)
        
        # Track alert
        self.total_alerts_sent += 1
        
        print(f"📢 Broadcasting alert to {len(self.active_connections)} client(s)...")
        
        # Send to all connections
        disconnected = set()
        for connection in self.active_connections:
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
    
    async def broadcast_token_alert(self, token_data: Dict[str, Any], scan_id: str):
        """
        Broadcast high-confidence token alert
        
        Args:
            token_data: Token prediction data
            scan_id: Scan ID for reference
        """
        alert = {
            "type": "token_alert",
            "scan_id": scan_id,
            "token": {
                "symbol": token_data.get("token_symbol"),
                "score": token_data.get("score"),
                "confidence": token_data.get("confidence"),
                "risk_level": token_data.get("risk_level"),
                "mentions": token_data.get("mention_count"),
                "sentiment": token_data.get("sentiment", {}).get("compound", 0),
                "contract": token_data.get("metrics", {}).get("contract_address"),
                "price_usd": token_data.get("metrics", {}).get("price_usd"),
                "market_cap": token_data.get("metrics", {}).get("market_cap"),
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
        sentiment = token_data.get("sentiment", {}).get("compound", 0)
        
        if confidence == "high":
            return f"🔥 HIGH confidence: ${symbol} detected (Score: {score:.1f}, Sentiment: {sentiment:.2f})"
        elif confidence == "medium":
            return f"⚠️ MEDIUM confidence: ${symbol} trending (Score: {score:.1f}, Sentiment: {sentiment:.2f})"
        else:
            return f"ℹ️ LOW confidence: ${symbol} detected (Score: {score:.1f}, Sentiment: {sentiment:.2f})"
    
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
