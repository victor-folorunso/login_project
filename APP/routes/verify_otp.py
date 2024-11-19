from fastapi import APIRouter, HTTPException
from prisma import Prisma
import pyotp
from APP.models import Verify_Otp_Model

VERIFY_OTP_ROUTER = APIRouter()
db = Prisma()


@VERIFY_OTP_ROUTER.get("/verify_otp")
async def verify_otp(otp_details: Verify_Otp_Model):
    email = otp_details.email
    try:
        await db.connect()
        selected_user = await db.user.find_unique(where={"email": email})
        otp = selected_user.otp
        key = selected_user.otp_secret

        totp = pyotp.TOTP(key, digits=6, interval=180)
        if totp.verify(otp):
            await db.user.update(
                where={"id": selected_user.id},
                data={"verified_email": True},
            )
            return f"your email has successfully been verified. user details: {selected_user}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        await db.disconnect()



