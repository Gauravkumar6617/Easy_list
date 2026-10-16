from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
import jwt
from datetime import datetime, timedelta ,timezone
from typing import Any, Union
from server.core.config import settings

pwd_hasher = PasswordHash(hashers=[BcryptHasher()])


def verify_password(plain_password, hashed_password):
    return pwd_hasher.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_hasher.hash(password)

def create_access_token(sub:Union[str, Any], expires_delta:Union[timedelta, int] = None):
    now = datetime.now(timezone.utc)

    if expires_delta is not None:
        if isinstance(expires_delta, int):
            expires_delta = timedelta(minutes=expires_delta)
        else:
            expires = now+expires_delta # Default to 30 minutes if not provided
    else:
        expires = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires, "sub": str(sub)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

def create_refresh_token(sub:Union[str, Any], expires_delta:Union[timedelta, int] = None):
    now = datetime.now(timezone.utc)

    if expires_delta is not None:
        if isinstance(expires_delta, int):
            expires_delta = timedelta(days=expires_delta)
        else:
            expires = now+expires_delta 
    else:
        expires = now + timedelta(days=7)

    to_encode = {"exp": expires, "sub": str(sub)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise Exception("Refresh token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid refresh token")