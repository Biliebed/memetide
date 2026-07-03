#!/usr/bin/env python3
"""
MemeTide FastAPI Server

API endpoints for memecoin trend prediction.
Built for OKX.AI Genesis Hackathon.
"""

import os
import time
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn

from src.engine import MemeTideEngine
from src.models import ScanResult
from src.websocket_manager import manager as ws_manager
from src.rate_limiter import RateLimitMiddleware, ws_rate_limiter
from src.auth import (
    get_current_user, require_premium, get_optional_user,
    User, create_access_token, authenticate_demo_user
)
from src.multichain import MultiChainDexScreener, Chain


# --- Request/Response Models ---

class ScanRequest(BaseModel):
    """Request body for scan endpoint"""
    min_mentions: int = Field(default=3, ge=1, le=100, description="Minimum mentions to consider a token")
    top_n: Optional[int] = Field(default=None, ge=1, le=50, description="Return only top N predictions")
    use_mock_data: bool = Field(default=False, description="Use mock Twitter data (for testing)")
    fetch_onchain: bool = Field(default=True, description="Fetch on-chain metrics from DexScreener")

class ScanResponse(BaseModel):
    """Response for scan endpoint"""
    status: str
    scan_id: str
    message: str
    data: Optional[dict] = None

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str
    uptime_seconds: float

class StatsResponse(BaseModel):
    """Statistics response"""
    total_scans: int
    total_tokens_analyzed: int
    average_scan_duration: float
    uptime_seconds: float


# --- In-memory storage (replace with DB in production) ---

scan_history: List[ScanResult] = []
server_start_time = time.time()


# --- Lifespan context ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    print("🌊 MemeTide API starting up...")
    print(f"   Time: {datetime.utcnow().isoformat()}")
    print(f"   Version: 1.2.0")
    print(f"   Features: REST API + WebSocket + Auth + Multi-chain + Rate Limiting")
    yield
    print("🌊 MemeTide API shutting down...")


# --- FastAPI app ---

app = FastAPI(
    title="MemeTide API",
    description="AI-powered memecoin trend prediction API with real-time WebSocket alerts, multi-chain support, and JWT authentication",
    version="1.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting middleware (60 requests/minute)
app.add_middleware(RateLimitMiddleware, requests_per_minute=60)

# Mount static files (web dashboard)
app.mount("/static", StaticFiles(directory="static"), name="static")


# --- Endpoints ---

@app.get("/", response_model=dict)
async def root():
    """Root endpoint - redirect to web dashboard"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")


@app.get("/api", response_model=dict)
async def api_info():
    """API info endpoint"""
    return {
        "name": "MemeTide API",
        "version": "1.2.0",
        "description": "AI-powered memecoin trend prediction with real-time alerts, multi-chain support, and authentication",
        "docs": "/docs",
        "dashboard": "/static/index.html",
        "websocket": "/ws/alerts",
        "alerts_demo": "/static/alerts.html",
        "features": {
            "realtime_alerts": True,
            "multichain": True,
            "authentication": True,
            "rate_limiting": True,
            "subscription_filters": True
        },
        "supported_chains": ["ethereum", "solana", "base", "arbitrum", "polygon", "bsc"],
        "endpoints": {
            "health": "/health",
            "scan": "/scan",
            "stats": "/stats",
            "history": "/history",
            "websocket": "/ws/alerts",
            "ws_stats": "/ws/stats",
            "auth_login": "/auth/login",
            "auth_me": "/auth/me",
            "multichain": "/token/multichain/{symbol}",
            "trending": "/trending/{chain}"
        },
        "hackathon": "OKX.AI Genesis Hackathon 2026"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.2.0",
        uptime_seconds=round(time.time() - server_start_time, 2)
    )


@app.post("/scan", response_model=ScanResponse)
async def scan_trends(request: ScanRequest):
    """
    Run memecoin trend scan
    
    **Process:**
    1. Scrape Twitter/X for crypto mentions
    2. Extract token symbols ($PEPE, $FLOKI, etc.)
    3. Analyze sentiment using AI
    4. Calculate risk & confidence scores
    5. Rank predictions by score
    
    **Returns:** Top trending memecoins with confidence levels
    """
    try:
        # Initialize engine
        engine = MemeTideEngine(
            use_mock_data=request.use_mock_data,
            fetch_onchain=request.fetch_onchain
        )
        
        # Run scan
        result = await engine.scan(min_mentions=request.min_mentions)
        
        # Store in history
        scan_history.append(result)
        
        # Broadcast alerts for high/medium confidence tokens
        for prediction in result.predictions[:3]:  # Top 3 only
            pred_dict = prediction if isinstance(prediction, dict) else prediction.__dict__
            if pred_dict.get("confidence") in ["high", "medium"]:
                await ws_manager.broadcast_token_alert(pred_dict, result.scan_id)
        
        # Broadcast scan complete
        await ws_manager.broadcast_scan_complete(result.to_dict())
        
        # Limit results if requested
        if request.top_n:
            result.predictions = result.predictions[:request.top_n]
        
        # Format response
        return ScanResponse(
            status="success",
            scan_id=result.scan_id,
            message=f"Scan complete. Found {result.unique_tokens} trending tokens.",
            data=result.to_dict()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")


@app.post("/scan/background", response_model=dict)
async def scan_trends_background(
    background_tasks: BackgroundTasks,
    request: ScanRequest
):
    """
    Run scan in background (non-blocking)
    
    Use this for long-running scans. Returns immediately with scan_id.
    Poll /history/{scan_id} to get results.
    """
    scan_id = f"bg-{int(time.time())}"
    
    async def run_scan():
        try:
            engine = MemeTideEngine(
                use_mock_data=request.use_mock_data,
                fetch_onchain=request.fetch_onchain
            )
            result = await engine.scan(min_mentions=request.min_mentions)
            scan_history.append(result)
        except Exception as e:
            print(f"Background scan {scan_id} failed: {e}")
    
    background_tasks.add_task(run_scan)
    
    return {
        "status": "processing",
        "scan_id": scan_id,
        "message": "Scan started in background. Poll /history for results.",
        "poll_url": f"/history?limit=1"
    }


@app.get("/history", response_model=dict)
async def get_scan_history(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    """Get scan history (paginated)"""
    total = len(scan_history)
    
    if total == 0:
        return {
            "total": 0,
            "limit": limit,
            "offset": offset,
            "results": []
        }
    
    # Reverse sort (newest first)
    sorted_history = sorted(
        scan_history,
        key=lambda x: x.timestamp,
        reverse=True
    )
    
    # Paginate
    paginated = sorted_history[offset:offset + limit]
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "results": [r.to_dict() for r in paginated]
    }


@app.get("/history/{scan_id}", response_model=dict)
async def get_scan_by_id(scan_id: str):
    """Get specific scan result by ID"""
    for result in scan_history:
        if result.scan_id == scan_id:
            return {
                "status": "found",
                "data": result.to_dict()
            }
    
    raise HTTPException(status_code=404, detail=f"Scan {scan_id} not found")


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get API statistics"""
    total_scans = len(scan_history)
    
    if total_scans == 0:
        avg_duration = 0.0
        total_tokens = 0
    else:
        avg_duration = sum(r.duration_seconds for r in scan_history) / total_scans
        total_tokens = sum(r.unique_tokens for r in scan_history)
    
    return StatsResponse(
        total_scans=total_scans,
        total_tokens_analyzed=total_tokens,
        average_scan_duration=round(avg_duration, 2),
        uptime_seconds=round(time.time() - server_start_time, 2)
    )


@app.delete("/history", response_model=dict)
async def clear_history():
    """Clear scan history (admin only - add auth in production)"""
    count = len(scan_history)
    scan_history.clear()
    return {
        "status": "success",
        "message": f"Cleared {count} scan results"
    }


# --- WebSocket Endpoints ---

@app.websocket("/ws/alerts")
async def websocket_alerts_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time alerts
    
    Connection: wss://memetide.app/ws/alerts
    
    Message Types:
    - connection: Initial connection confirmation
    - token_alert: High-confidence token detected
    - scan_complete: Scan finished notification
    
    Client Commands:
    - ping → pong
    - {"command": "stats"} → Get WS stats
    - {"command": "subscribe", "tokens": ["PEPE", "FLOKI"]} → Filter alerts
    - {"command": "unsubscribe"} → Receive all alerts
    """
    client_id = websocket.query_params.get("client_id", "")
    
    # Get client IP for rate limiting
    client_ip = "unknown"
    if websocket.client:
        client_ip = websocket.client.host
    
    # Check rate limit (max connections per IP)
    if not ws_rate_limiter.can_connect(client_ip):
        await websocket.close(code=1008, reason="Too many connections from this IP")
        return
    
    try:
        # Connect client
        await ws_manager.connect(websocket, client_id)
        ws_rate_limiter.register_connection(client_ip)
        
        # Keep connection alive
        while True:
            # Wait for client messages (ping/pong or commands)
            try:
                data = await websocket.receive_text()
                
                # Handle ping
                if data == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                
                # Handle commands
                elif data.startswith("{"):
                    import json
                    message = json.loads(data)
                    command = message.get("command")
                    
                    if command == "stats":
                        stats = ws_manager.get_stats()
                        await ws_manager.send_personal_message({
                            "type": "stats",
                            "data": stats
                        }, websocket)
                    
                    elif command == "subscribe":
                        # Subscribe to specific tokens
                        tokens = message.get("tokens", [])
                        if tokens:
                            ws_manager.subscribe(websocket, set(tokens))
                            await ws_manager.send_personal_message({
                                "type": "subscribed",
                                "tokens": tokens,
                                "message": f"Subscribed to {len(tokens)} token(s)"
                            }, websocket)
                        else:
                            await ws_manager.send_personal_message({
                                "type": "error",
                                "message": "No tokens specified"
                            }, websocket)
                    
                    elif command == "unsubscribe":
                        # Unsubscribe (receive all alerts)
                        ws_manager.unsubscribe(websocket)
                        await ws_manager.send_personal_message({
                            "type": "unsubscribed",
                            "message": "Now receiving all alerts"
                        }, websocket)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                print(f"WebSocket error: {e}")
                break
    
    finally:
        ws_manager.disconnect(websocket)
        ws_rate_limiter.unregister_connection(client_ip)


@app.get("/ws/stats", response_model=dict)
async def websocket_stats():
    """Get WebSocket connection statistics"""
    return {
        "status": "success",
        "data": ws_manager.get_stats()
    }


# --- Authentication Endpoints ---

@app.post("/auth/login", response_model=dict)
async def login(username: str, password: str):
    """
    Demo login endpoint
    
    **Demo Accounts:**
    - Free: username=demo_free, password=free123
    - Premium: username=demo_premium, password=premium123
    """
    token = authenticate_demo_user(username, password)
    
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "message": "Login successful"
    }


@app.get("/auth/me", response_model=dict)
async def get_user_info(user: User = Depends(get_current_user)):
    """Get current user info"""
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return {
        "user_id": user.user_id,
        "tier": user.tier,
        "scans_remaining": user.scans_remaining
    }


# --- Multi-chain Endpoints ---

@app.get("/token/multichain/{symbol}", response_model=dict)
async def get_token_multichain(
    symbol: str,
    chains: Optional[str] = Query(None, description="Comma-separated chain list (ethereum,solana,base)")
):
    """
    Search token across multiple chains
    
    **Example:** /token/multichain/PEPE?chains=ethereum,solana,base
    """
    try:
        dex = MultiChainDexScreener()
        
        # Parse chains
        chain_list = None
        if chains:
            chain_names = [c.strip().lower() for c in chains.split(",")]
            chain_list = [Chain(name) for name in chain_names if name in [e.value for e in Chain]]
        
        results = await dex.search_token_multi_chain(symbol, chain_list)
        
        return {
            "status": "success",
            "symbol": symbol,
            "chains_searched": len(chain_list) if chain_list else 3,
            "results_found": len(results),
            "data": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Multi-chain search failed: {str(e)}")


@app.get("/trending/{chain}", response_model=dict)
async def get_trending_by_chain(
    chain: str,
    limit: int = Query(default=10, ge=1, le=50)
):
    """
    Get trending tokens on specific chain
    
    **Supported chains:** ethereum, solana, base, arbitrum, polygon, bsc
    """
    try:
        chain_enum = Chain(chain.lower())
        dex = MultiChainDexScreener()
        
        results = await dex.get_trending_pairs(chain_enum, limit)
        
        return {
            "status": "success",
            "chain": chain,
            "count": len(results),
            "data": results
        }
    
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid chain: {chain}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get trending: {str(e)}")


# --- Error handlers ---

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Catch-all error handler"""
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# --- Main entry point ---

if __name__ == "__main__":
    import os
    
    # Get port from environment (Railway, Render, Fly.io set this)
    port = int(os.getenv("PORT", 8000))
    
    print("\n" + "="*60)
    print("🌊 MEMETIDE API SERVER")
    print("="*60)
    print("Starting FastAPI server...")
    print(f"Port: {port}")
    print(f"Docs: http://0.0.0.0:{port}/docs")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
