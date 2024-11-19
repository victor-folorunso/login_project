from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException
from prisma import Prisma
from APP.functions import create_access_token, verify_password
from APP.models import User_Detail_Model
from APP.otp_manager.otp_main import send_email_confirmation_link

LOGIN_ROUTER = APIRouter()
db = Prisma()

@LOGIN_ROUTER.post("/login")
async def login(user_details: User_Detail_Model):
    try:
        await db.connect()
        user = await db.user.find_unique(where={"email": user_details.email})
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect Email or password")

        if not verify_password(user_details.password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect Email or password")
        
        if not (user.email_verified):
            otp_secret = user.otp_secret
            otp = send_email_confirmation_link(user_details.email,otp_secret)
           
            await db.user.update(
                where={"id": user.id},
                data={"otp": otp},
            )
            message = f"email not verified. a confirmation mail has been sent to {user_details.email}"
            raise HTTPException(status_code=401, detail=message)
        

        expire_time = datetime.now(timezone.utc) + timedelta(days=7)
        token = create_access_token({"sub": user.email},expire_time)
        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await db.disconnect()
