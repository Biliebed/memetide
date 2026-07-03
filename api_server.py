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
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

from src.engine import MemeTideEngine
from src.models import ScanResult


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
    print(f"   Version: 1.0.0")
    yield
    print("🌊 MemeTide API shutting down...")


# --- FastAPI app ---

app = FastAPI(
    title="MemeTide API",
    description="AI-powered memecoin trend prediction API",
    version="1.0.0",
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


# --- Endpoints ---

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API info"""
    return {
        "name": "MemeTide API",
        "version": "1.0.0",
        "description": "AI-powered memecoin trend prediction",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "scan": "/scan",
            "stats": "/stats",
            "history": "/history"
        },
        "hackathon": "OKX.AI Genesis Hackathon 2026"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
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
