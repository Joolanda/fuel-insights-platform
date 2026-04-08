from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import requests

KEYCLOAK_ISSUER = "http://localhost:8080/realms/fuel-insights"
JWKS_URL = f"{KEYCLOAK_ISSUER}/protocol/openid-connect/certs"

security = HTTPBearer()
JWKS_CACHE = None

def get_jwks():
    global JWKS_CACHE
    if JWKS_CACHE is None:
        JWKS_CACHE = requests.get(JWKS_URL).json()
    return JWKS_CACHE

def decode_token(token: str):
    jwks = get_jwks()

    try:
        unverified_header = jwt.get_unverified_header(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token header")

    kid = unverified_header.get("kid")
    key = next((k for k in jwks["keys"] if k["kid"] == kid), None)

    if not key:
        raise HTTPException(status_code=401, detail="Invalid token key")

    try:
        # decode zonder audience-check
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            issuer=KEYCLOAK_ISSUER,
            options={"verify_aud": False}
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    # flexibele audience-check
    aud = payload.get("aud")
    allowed = ["account", "fuel-api"]

    if isinstance(aud, str):
        if aud not in allowed:
            raise HTTPException(status_code=401, detail="Invalid audience")
    elif isinstance(aud, list):
        if not any(a in allowed for a in aud):
            raise HTTPException(status_code=401, detail="Invalid audience")

    return payload


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)

    roles = payload.get("realm_access", {}).get("roles", [])
    username = payload.get("preferred_username", "unknown")

    return {"username": username, "roles": roles}

def require_role(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        if required_role not in user["roles"]:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_checker
