# aibe/ui/backend/middleware/security.py
"""Security middleware for FastAPI application."""

from __future__ import annotations

import os
import time
from collections import defaultdict
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    }

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        for header, value in self.SECURITY_HEADERS.items():
            response.headers[header] = value

        # Add HSTS in production
        if os.getenv("ENVIRONMENT") == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware."""

    def __init__(self, app, requests_per_minute: int = 100) -> None:
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self._request_counts: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip rate limiting for health checks
        if request.url.path in ("/api/health", "/metrics"):
            return await call_next(request)

        client_ip = self._get_client_ip(request)
        current_time = time.time()
        window_start = current_time - 60

        # Clean old requests
        self._request_counts[client_ip] = [
            t for t in self._request_counts[client_ip]
            if t > window_start
        ]

        # Check rate limit
        if len(self._request_counts[client_ip]) >= self.requests_per_minute:
            retry_after = int(60 - (current_time - self._request_counts[client_ip][0]))
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"},
                headers={"Retry-After": str(max(1, retry_after))},
            )

        # Record request
        self._request_counts[client_ip].append(current_time)

        return await call_next(request)

    @staticmethod
    def _get_client_ip(request: Request) -> str:
        """Extract client IP from request."""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"


class APIKeyMiddleware(BaseHTTPMiddleware):
    """Optional API key authentication middleware."""

    def __init__(self, app, api_key: str | None = None) -> None:
        super().__init__(app)
        self.api_key = api_key or os.getenv("API_KEY")
        self.enabled = os.getenv("API_KEY_REQUIRED", "false").lower() == "true"

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip if not enabled
        if not self.enabled or not self.api_key:
            return await call_next(request)

        # Skip for health endpoint
        if request.url.path == "/api/health":
            return await call_next(request)

        # Check authorization header
        auth_header = request.headers.get("Authorization", "")
        
        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid authorization header"},
            )

        token = auth_header[7:]  # Remove "Bearer " prefix
        
        if token != self.api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid API key"},
            )

        return await call_next(request)