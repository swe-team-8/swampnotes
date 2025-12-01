from __future__ import annotations
from typing import Optional, TypedDict, Any

from fastapi import Header, HTTPException, Depends, status
from jwt import decode as jwt_decode, InvalidTokenError, PyJWKClient

from .settings import settings

# NOTE: jwt_handler.py has been consolidated within this file


class TokenUser(TypedDict, total=False):
    sub: str
    name: Optional[str]
    email: Optional[str]
    username: str
    role: Optional[str]
    is_admin: Optional[Any]


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
    """
    Verify Clerk-issued RS256 JWT.
    Returns claims dict with sub/email/name/role/is_admin or None if no Authorization header.
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
        # Include role and is_admin from claims
        return {
            "sub": claims.get("sub", ""),
            "name": name,
            "email": email,
            "username": claims.get("username"),
            "role": claims.get("role"),
            "is_admin": claims.get("is_admin"),
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
    """
    Enforce admin access based on JWT claims: role or is_admin.
    Allowed roles: admin, dev, developer, superadmin.
    """
    # Get raw claims from current user - we need to decode the token again to access custom claims
    # Note: current is already validated by require_user, so we trust the sub/email
    # We'll need to pass the full decoded claims through. For now, read from a request-scoped cache or re-decode.

    # Simplified approach: assume you store full claims in get_current_user
    # If not, you can refactor to return full claims dict and type narrow to TokenUser where needed

    # For now, let's assume you modify get_current_user to return all claims
    # and we check role/is_admin here:

    role = current.get("role") or current.get("roles") or current.get("user_role")
    is_admin_claim = current.get("is_admin")

    allowed_roles = {"admin", "dev", "developer", "superadmin"}
    has_role = isinstance(role, str) and role.strip().lower() in allowed_roles
    has_admin_flag = _truthy(is_admin_claim)

    if not (has_role or has_admin_flag):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return current


def _truthy(val: Any) -> bool:
    # Helper to interpret various truthy values from JWT claims.
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return val == 1
    if isinstance(val, str):
        return val.strip().lower() in {"1", "true", "yes", "y"}
    return False


# Export these names when auth_clerk.py is imported via wildcard (*)
# wildcard imports are bad practice though, so try not to use them in general
__all__ = [
    "TokenUser",
    "get_current_user",
    "require_user",
    "optional_user",
    "require_admin",
]
