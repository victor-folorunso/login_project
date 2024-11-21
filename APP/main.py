from datetime import timedelta, timezone
from logging.handlers import RotatingFileHandler
from fastapi import Depends, FastAPI, HTTPException
from prisma import Prisma
import logging
from .models import *
from .functions import *

log_handler = RotatingFileHandler("error.log",maxBytes=2048)
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[log_handler]
)
app = FastAPI(
    debug=False,
    title="login project API",
    version="0.0.1",
    description="This is a full login / sign up API with advanced features and security without sacrificing code simplicity.\nIt is built using fastapi at its core,uvicorn, mysql, and python prisma ORM.\n\nIt is supposed to be a reusable code and serves as part of larger projects.",
)
db = Prisma()

@app.post("/admin/show_all_users")
async def show_all_users(user_details: User_Detail_Model):
    email = user_details.email
    try:
        await db.connect()
        current_user = await db.user.find_unique(where={"email": email})
       
        if current_user.role != "admin":
            logging.error("403 (forbidden). Admin priviledge required to access this endpoint")
            raise HTTPException(status_code=403)  
        if not  current_user:
            raise HTTPException(status_code=400, detail="Incorrect Email or password")

        if not verify_password(user_details.password, current_user.password):
            raise HTTPException(status_code=400, detail="Incorrect Email or password")

        if not (current_user.email_verified):
            otp_secret = current_user.otp_secret
            otp = send_email_confirmation_link(user_details.email, otp_secret)

            await db.user.update(
                where={"id": current_user.id},
                data={"otp": otp},
            )
            message = f"email not verified. a confirmation mail has been sent to {user_details.email}"
            raise HTTPException(status_code=401, detail=message)

        users = await db.user.find_many()
        return users
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=401)
    finally:
        await db.disconnect()

@app.post("/admin/delete_all_users")
async def delete_all_users(user_details: User_Detail_Model):
    email = user_details.email
    try:
        await db.connect()
        current_user = await db.user.find_unique(where={"email": email})
       
        if current_user.role != "admin":
            logging.error("403 (forbidden). Admin priviledge required to access this endpoint")
            raise HTTPException(status_code=403)  
        if not  current_user:
            raise HTTPException(status_code=400, detail="Incorrect Email or password")

        if not verify_password(user_details.password, current_user.password):
            raise HTTPException(status_code=400, detail="Incorrect Email or password")

        if not (current_user.email_verified):
            otp_secret = current_user.otp_secret
            otp = send_email_confirmation_link(user_details.email, otp_secret)

            await db.user.update(
                where={"id": current_user.id},
                data={"otp": otp},
            )
            message = f"email not verified. a confirmation mail has been sent to {user_details.email}"
            raise HTTPException(status_code=401, detail=message)

        await db.user.delete_many()
        return "deleted all users"
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=401)
    finally:
        await db.disconnect()

@app.post("/verify_email")
async def verify_email(otp_details: Verify_Email_Model):
    email = otp_details.email
    try:
        await db.connect()
        selected_user = await db.user.find_unique(where={"email": email})

        if not selected_user:
            raise HTTPException(status_code=400, detail="Incorrect Email or password")

        if not (selected_user.email_verified):
            otp_secret = selected_user.otp_secret
            otp = send_email_confirmation_link(otp_details.email, otp_secret)

            await db.user.update(
                where={"id": selected_user.id},
                data={"otp": otp},
            )
            message = f"email not verified. a confirmation mail has been sent to {selected_user.email}"
            raise HTTPException(status_code=401, detail=message)
           
        
        otp = selected_user.otp
        key = selected_user.otp_secret

        totp = pyotp.TOTP(key, digits=8, interval=600)
        if totp.verify(otp):
            await db.user.update(
                where={"id": selected_user.id},
                data={"email_verified": True},
            )
            return "your email has successfully been verified"
        raise HTTPException(status_code=401, detail="invalid or expired otp")
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=401)
    finally:
        await db.disconnect()

@app.post("/reset_password")
async def reset_password(reset_password_details: Reset_Password_Model):
    email = reset_password_details.email
    try:
        await db.connect()
        selected_user = await db.user.find_unique(where={"email": email})
        if not selected_user:
            raise HTTPException(status_code=400, detail="Incorrect Email or password")

        if not (selected_user.email_verified):
            otp_secret = selected_user.otp_secret
            otp = send_email_confirmation_link(reset_password_details.email, otp_secret)

            await db.user.update(
                where={"id": selected_user.id},
                data={"otp": otp},
            )
            message = f"email not verified. a confirmation mail has been sent to {selected_user.email}"
            raise HTTPException(status_code=401, detail=message)
        
        otp = selected_user.otp
        key = selected_user.otp_secret

        totp = pyotp.TOTP(key, digits=8, interval=600)
        if totp.verify(otp):
            hashed_pswd = hash_password(reset_password_details.new_password)
            await db.user.update(
                where={"id": selected_user.id},
                data={ "password": hashed_pswd,},
            )
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=401)

    finally:
        await db.disconnect()

@app.post("/login")
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
            otp = send_email_confirmation_link(user_details.email, otp_secret)

            await db.user.update(
                where={"id": user.id},
                data={"otp": otp},
            )
            message = f"email not verified. a confirmation mail has been sent to {user_details.email}"
            raise HTTPException(status_code=401, detail=message)

        expire_time = datetime.now(timezone.utc) + timedelta(days=7)
        token = create_access_token({"sub": user.email}, expire_time)
        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=401)
    finally:
        await db.disconnect()

@app.post("/sign_up")
async def sign_up(user_details: User_Detail_Model):
    email = user_details.email
    try:
        await db.connect()

        existing_user = await db.user.find_unique(where={"email": email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        otp_secret = gen_otp_secret()
        otp = send_email_confirmation_link(email, otp_secret)
        hashed_pswd = hash_password(user_details.password)

        await db.user.create(
            data={
                "email": email,
                "password": hashed_pswd,
                "otp": otp,
                "otp_secret": otp_secret,
                "role": "admin"
            }
        )

        text = f"a confirmation link has been sent to {email}. click on it to activate your account"
        return {"message": text}

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=401)
    finally:
        await db.disconnect()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}

@app.get("/homepage")
async def homepage(current_user: str = Depends(validate_jwt)):
    return "homepage. current user is " + current_user

