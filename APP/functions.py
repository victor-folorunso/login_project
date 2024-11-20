from dotenv import load_dotenv
from fastapi import HTTPException
from passlib.context import CryptContext
import os
from datetime import datetime
from jose import JWTError, jwt
import yagmail
import pyotp
from pydantic import EmailStr


def send_email_confirmation_link(email: EmailStr, otp_secret: str):
    otp = str(gen_otp(otp_secret))
    
    html_content = f"""
    <html>
    <p>thanks for signing up</p>
    <p>your otp is <b>{otp}</b></p>
    </html>
    """
    try:
        setup_yagmail()
        send_email(to_email=email, subject="otp", body=html_content)
        return otp
    except:
        raise HTTPException(status_code=400, detail=str("most likely a network error when sending the email"))



def gen_otp(key: str):
    load_dotenv()
    totp = pyotp.TOTP(key, digits=8, interval=600)
    otp = totp.now()
    return otp


def gen_otp_secret():
    secret = pyotp.random_base32()
    return secret


def setup_yagmail():
    load_dotenv()
    email = "victorfolorunsoofficial@gmail.com"
    app_password = os.getenv("GMAIL_APP_PASSWORD")
    yagmail.register(email, app_password)


def send_email(to_email: str, subject: str, body: str):
    yag = yagmail.SMTP("victorfolorunsoofficial@gmail.com")
    yag.send(
        to=to_email,
        subject=subject,
        contents=body,
        headers={"from": "login project"},
    )


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
