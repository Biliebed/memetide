#!/usr/bin/env python3
"""
JWT Authentication for MemeTide API

Provides optional authentication for premium features.
Free tier: 10 scans/day, no WebSocket
Premium tier: Unlimited scans, WebSocket alerts, API access
"""

import os
import jwt
import time
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel


# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "memetide-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


class TokenData(BaseModel):
    """JWT token payload"""
    user_id: str
    tier: str  # "free" or "premium"
    expires_at: float


class User(BaseModel):
    """User model"""
    user_id: str
    tier: str
    scans_remaining: Optional[int] = None  # None = unlimited (premium)


security = HTTPBearer(auto_error=False)


def create_access_token(user_id: str, tier: str = "free") -> str:
    """
    Create JWT access token
    
    Args:
        user_id: Unique user identifier
        tier: "free" or "premium"
    
    Returns:
        JWT token string
    """
    expires_at = time.time() + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    
    payload = {
        "user_id": user_id,
        "tier": tier,
        "exp": expires_at,
        "iat": time.time()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str) -> TokenData:
    """
    Verify JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        TokenData if valid
    
    Raises:
        HTTPException if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        return TokenData(
            user_id=payload["user_id"],
            tier=payload["tier"],
            expires_at=payload["exp"]
        )
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[User]:
    """
    Get current authenticated user (optional)
    
    Returns:
        User if authenticated, None if no token (free tier)
    """
    # No token = free tier access
    if not credentials:
        return None
    
    # Verify token
    token_data = verify_token(credentials.credentials)
    
    return User(
        user_id=token_data.user_id,
        tier=token_data.tier,
        scans_remaining=None if token_data.tier == "premium" else 10
    )


async def require_premium(
    user: Optional[User] = Depends(get_current_user)
) -> User:
    """
    Require premium tier authentication
    
    Raises:
        HTTPException if not premium
    """
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Premium subscription required. Get access at /auth/premium"
        )
    
    if user.tier != "premium":
        raise HTTPException(
            status_code=403,
            detail="Premium subscription required for this feature"
        )
    
    return user


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[User]:
    """
    Get user if authenticated, allow anonymous otherwise
    
    Use this for endpoints that work for both free & premium
    """
    if not credentials:
        return User(user_id="anonymous", tier="free", scans_remaining=10)
    
    try:
        token_data = verify_token(credentials.credentials)
        return User(
            user_id=token_data.user_id,
            tier=token_data.tier,
            scans_remaining=None if token_data.tier == "premium" else 10
        )
    except HTTPException:
        # Invalid token = treat as free tier
        return User(user_id="anonymous", tier="free", scans_remaining=10)


# Demo users (in production, use database)
DEMO_USERS = {
    "demo_free": {"tier": "free", "password": "free123"},
    "demo_premium": {"tier": "premium", "password": "premium123"}
}


def authenticate_demo_user(username: str, password: str) -> Optional[str]:
    """
    Authenticate demo user and return token
    
    In production, replace with real auth (OAuth, email/password, etc.)
    """
    user = DEMO_USERS.get(username)
    if not user or user["password"] != password:
        return None
    
    return create_access_token(username, user["tier"])
