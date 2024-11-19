from fastapi import APIRouter, HTTPException
from prisma import Prisma
from APP.functions import hash_password
from APP.models import User_Detail_Model
from APP.otp_manager.otp_gen import gen_otp_secret
from APP.otp_manager.otp_main import send_email_confirmation_link

SIGNUP_ROUTER = APIRouter()
db = Prisma()


@SIGNUP_ROUTER.post("/sign_up")
async def sign_up(user_details: User_Detail_Model):
    email = user_details.email
    try:
        await db.connect()

        existing_user = await db.user.find_unique(where={"email": email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        otp_secret = gen_otp_secret()
        otp = send_email_confirmation_link(email,otp_secret)
        hashed_pswd = hash_password(user_details.password)

        await db.user.create(
            data={
                "email": email,
                "password": hashed_pswd,
                "otp": otp,
                "otp_secret": otp_secret,
            }
        )

        text = f"a confirmation link has been sent to {email}. click on it to activate your account"
        return {"message": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        await db.disconnect()





