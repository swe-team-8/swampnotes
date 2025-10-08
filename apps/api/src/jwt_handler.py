import jwt
import time
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# These values are supposed to be in a .env file, but for some reason,
# Creating a .env conflicted with the settings module in main.py
# and crashed the server.
SECRET = "4df3bc783e6dc21b74023f7b40a3ef94009c79a550a93cdc19e7439d5d5e3e3f"
ALGO = "HS256"
EXPIRATION = 3600 # One Hour


# This functions signs a jwt and returns it to the user
# Should be called right after login/signup
# Response should be saved as a variable in js and used
# For things like making transactions, posting notes, etc.
def sign(userID: str, is_admin: bool):
    payload = {
        "userID": userID,
        "admin": is_admin,
        "expiration": time.time() + EXPIRATION
    }
    return {"User Token": jwt.encode(payload, SECRET, algorithm=ALGO)}


# Verifies that token is valid.
def decode(token: str):
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGO])
    except jwt.ExpiredSignatureError:
        return {"Error": "Your token has expired, please sign in again."}
    # except jwt.InvalidTokenError:
    #     return {"Error": "Invalid token, please sign in again."}


# To be clear, I don't fully understand how this class works.
# But it offloads a lot of the verification process to FastAPI.
class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error: bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)

    async def __call__(self, request: Request):
        credentials : HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code = 403)
            return credentials.credentials
        else:
            raise HTTPException(status_code = 403)

    def verify_jwt(self, jwtoken: str):
        isTokenValid : bool = False
        payload = decode(jwtoken)
        if payload:
            isTokenValid = True
        return isTokenValid