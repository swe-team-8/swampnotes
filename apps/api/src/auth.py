from __future__ import annotations
from typing import Optional, TypedDict

from fastapi import Header, HTTPException, Depends, status
from jwt import decode as jwt_decode, InvalidTokenError, PyJWKClient

from .settings import settings

# NOTE: jwt_handler.py has been consolidated within this file


class TokenUser(TypedDict, total=False):
    sub: str
    name: Optional[str]
    email: Optional[str]
    username: str


# Caches JWK client across requests
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

    # cache a single client instance (httpx.Client used for timeouts/reuse)
    if _jwk_client is None or _jwk_client.uri != url:
        _jwk_client = PyJWKClient(url, timeout=5)
    return _jwk_client


async def get_current_user(
    authorization: str | None = Header(None),
) -> Optional[TokenUser]:
    print(authorization)
    """
    Verify Clerk-issued RS256 JWT.
    Returns claims (sub/email) or None if no Authorization header.
    Should also raise 401 if an invalid bearer token is present
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
        name = claims.get("name")
        email = (
            claims.get("email")
            or claims.get("email_address")
            or claims.get("clerk_email")
        )
        return {
            "sub": claims.get("sub", ""),
            "name": name,
            "email": email,
            "username": claims.get("username"),
        }
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")


# Use this hard auth to require a valid user
def require_user(current: Optional[TokenUser] = Depends(get_current_user)):
    if not current:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Sign in required"
        )
    return current


# Use this to expose the user (can be None) to routes w/ optional auth
def optional_user(
    current: Optional[TokenUser] = Depends(get_current_user),
) -> Optional[TokenUser]:
    return current


# This is a placeholder for role-based access control. When we have persistent roles in the DB, we can enforce 'admin' here
def require_admin(current: TokenUser = Depends(require_user)) -> TokenUser:
    # TODO: look up role in DB, 403 if not admin
    return current


# Export these names when auth_clerk.py is imported via wildcard (*)
# wildcard imports are bad practice though, so try not to use them in general
__all__ = [
    "TokenUser",
    "get_current_user",
    "require_user",
    "optional_user",
    "require_admin",
]
