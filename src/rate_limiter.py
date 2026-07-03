#!/usr/bin/env python3
"""
Rate Limiting Middleware

Implements token bucket algorithm for API rate limiting.
"""

import time
from typing import Dict, Tuple
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        burst_size: int = 10
    ):
        self.rate = requests_per_minute / 60.0  # requests per second
        self.burst_size = burst_size
        
        # client_id -> (tokens, last_update)
        self.buckets: Dict[str, Tuple[float, float]] = defaultdict(
            lambda: (float(burst_size), time.time())
        )
    
    def _get_client_id(self, request: Request) -> str:
        """Extract client identifier from request"""
        # Try to get from X-Forwarded-For (Railway/proxy)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        # Fallback to direct client
        if request.client:
            return request.client.host
        
        return "unknown"
    
    def is_allowed(self, client_id: str) -> Tuple[bool, float]:
        """
        Check if request is allowed
        
        Returns:
            (allowed, retry_after_seconds)
        """
        tokens, last_update = self.buckets[client_id]
        now = time.time()
        
        # Refill tokens based on time elapsed
        elapsed = now - last_update
        tokens = min(self.burst_size, tokens + elapsed * self.rate)
        
        if tokens >= 1.0:
            # Allow request, consume token
            self.buckets[client_id] = (tokens - 1.0, now)
            return True, 0.0
        else:
            # Deny request, calculate retry time
            retry_after = (1.0 - tokens) / self.rate
            self.buckets[client_id] = (tokens, now)
            return False, retry_after
    
    async def __call__(self, request: Request) -> bool:
        """Check rate limit for request"""
        client_id = self._get_client_id(request)
        allowed, retry_after = self.is_allowed(client_id)
        
        if not allowed:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Retry after {retry_after:.1f} seconds.",
                headers={"Retry-After": str(int(retry_after) + 1)}
            )
        
        return True


class RateLimitMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware for rate limiting"""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.limiter = RateLimiter(requests_per_minute=requests_per_minute)
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks and static files
        if request.url.path in ["/health", "/", "/api"] or request.url.path.startswith("/static"):
            return await call_next(request)
        
        # Check rate limit
        try:
            await self.limiter(request)
        except HTTPException as e:
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=e.status_code,
                content={"error": e.detail},
                headers=e.headers
            )
        
        return await call_next(request)


# WebSocket rate limiter (separate from HTTP)
class WebSocketRateLimiter:
    """Rate limiter for WebSocket connections"""
    
    def __init__(self, max_connections_per_ip: int = 5):
        self.max_connections = max_connections_per_ip
        # ip -> connection_count
        self.connections: Dict[str, int] = defaultdict(int)
    
    def can_connect(self, client_ip: str) -> bool:
        """Check if client can open new connection"""
        return self.connections[client_ip] < self.max_connections
    
    def register_connection(self, client_ip: str):
        """Register new connection"""
        self.connections[client_ip] += 1
    
    def unregister_connection(self, client_ip: str):
        """Unregister closed connection"""
        if self.connections[client_ip] > 0:
            self.connections[client_ip] -= 1
        
        # Clean up if no connections
        if self.connections[client_ip] == 0:
            del self.connections[client_ip]
    
    def get_stats(self) -> Dict:
        """Get rate limiter stats"""
        return {
            "total_ips": len(self.connections),
            "total_connections": sum(self.connections.values()),
            "max_per_ip": self.max_connections,
            "top_ips": sorted(
                self.connections.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }


# Global instances
ws_rate_limiter = WebSocketRateLimiter(max_connections_per_ip=5)
