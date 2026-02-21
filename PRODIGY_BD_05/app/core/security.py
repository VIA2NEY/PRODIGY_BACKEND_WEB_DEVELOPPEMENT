from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings

# Configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def get_current_user(credentials = Depends(security)):
    """
    Returns the current user based on the given credentials.

    Args:
        credentials: The authorization credentials.

    Returns:
        The current user.

    Raises:
        HTTPException: If the credentials are invalid.
    """
    return verify_token(credentials)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifier un mot de passe"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hacher un mot de passe"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Créer un token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials) -> dict:
    """Vérifier un token JWT"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")
        if username is None or user_id is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": 401,
                    "message": "Token invalide",
                    "data": None,
                },
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username, "user_id": user_id, "role": role,}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": 401,
                "message": "Token invalide or expired",
                "data": None,
            },
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_roles(*require_roles: str):
    """
    Require a user to have one of the given roles.

    This function will return a FastAPI dependency that will check if the current user has one of the given roles.
    If the user does not have one of the given roles, it will raise an HTTPException with a 403 status code.

    The dependency will return the current user if the check is successful.

    :param require_roles: A variable number of roles to require.
    :return: A FastAPI dependency that checks if a user has one of the given roles.
    """
    def role_checker(current_user = Depends(get_current_user)):
        if current_user["role"] not in require_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": 403,
                    "message": "Access forbidden",
                    "data": None,
                },
            )
        return current_user

    return role_checker