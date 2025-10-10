from __future__ import annotations
from typing import Optional, TypedDict

import httpx
from fastapi import Header, HTTPException
from jwt import decode as jwt_decode, InvalidTokenError, PyJWKClient

from .settings import settings


class TokenUser(TypedDict, total=False):
    sub: str
    email: Optional[str]


_jwk_client: Optional[PyJWKClient] = None


def _jwks_url() -> str:
    if settings.AUTH_JWKS_URL:
        return settings.AUTH_JWKS_URL
    if not settings.AUTH_ISSUER:
        raise HTTPException(status_code=500, detail="AUTH_ISSUER not configured")
    base = settings.AUTH_ISSUER.rstrip("/")
    return f"{base}/.well-known/jwks.json"


def _get_jwk_client() -> PyJWKClient:
    global _jwk_client
    url = _jwks_url()

    # cache a single client instance
    if _jwk_client is None or _jwk_client.uri != url:
        _jwk_client = PyJWKClient(url, session=httpx.Client(timeout=5))
    return _jwk_client


async def get_current_user(
    authorization: str | None = Header(None),
) -> Optional[TokenUser]:
    """
    Verify Clerk-issued RS256 JWT.
    Returns claims (sub/email) or None if no Authorization header.
    """
    if not authorization or not authorization.lower().startswith("bearer "):
        return None

    token = authorization.split(" ", 1)[1]
    try:
        jwk_client = _get_jwk_client()
        signing_key = jwk_client.get_signing_key_from_jwt(token).key

        claims = jwt_decode(
            token,
            signing_key,
            algorithms=["RS256"],
            audience=settings.AUTH_AUDIENCE,
            issuer=settings.AUTH_ISSUER,
            options={"require": ["exp", "iss", "aud"]},
        )
        email = (
            claims.get("email")
            or claims.get("email_address")
            or claims.get("clerk_email")
        )
        return {"sub": claims.get("sub", ""), "email": email}
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
