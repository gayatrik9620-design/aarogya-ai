import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone

import jwt

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "CHANGE_THIS_SECRET_BEFORE_DEPLOYMENT"
)

ALGORITHM = "HS256"

TOKEN_MINUTES = 60 * 12

bearer = HTTPBearer()


# Password Encryption
def hash_password(password: str):

    salt = os.urandom(16)

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        180000
    )

    return salt.hex() + ":" + digest.hex()


# Verify Password
def verify_password(password: str, stored: str):

    try:
        salt_hex, digest_hex = stored.split(":")

        actual = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            bytes.fromhex(salt_hex),
            180000
        ).hex()

        return hmac.compare_digest(actual, digest_hex)

    except (ValueError, TypeError):
        return False


# Generate Login Token
def create_access_token(user_id: int):

    expiry = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_MINUTES
    )

    return jwt.encode(
        {
            "sub": str(user_id),
            "exp": expiry
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# Get Logged-in User
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer)
):

    from backend.database import get_connection

    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = int(payload["sub"])

    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    with get_connection() as conn:

        user = conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return dict(user)