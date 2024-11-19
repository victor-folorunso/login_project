
from dotenv import load_dotenv
import pyotp

def gen_otp(key: str):
  load_dotenv()
  totp = pyotp.TOTP(key, digits=6, interval=180)
  otp = totp.now()
  return otp

def gen_otp_secret():
  secret = pyotp.random_base32()
  return secret