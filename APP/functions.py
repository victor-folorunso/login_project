from dotenv import load_dotenv
from fastapi import HTTPException
from passlib.context import CryptContext
import os
from datetime import datetime
from jose import JWTError, jwt


def hash_password(password: str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"])
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_context = CryptContext(schemes=["bcrypt"])
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expire: datetime) -> str:
    load_dotenv()
    key = os.getenv("SECRET_KEY")
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm="HS256")
    return encoded_jwt


async def validate_jwt(token: str):
    load_dotenv()
    key = os.getenv("SECRET_KEY")
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, key, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception
    
