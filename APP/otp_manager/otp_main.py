from fastapi import HTTPException
from pydantic import EmailStr
from APP.otp_manager.mail_sender import send_email, setup_yagmail
from APP.otp_manager.otp_gen import gen_otp


def send_email_confirmation_link(email: EmailStr, otp_secret: str):
    otp = str(gen_otp(otp_secret))

    obfuscated_otp = otp
    obfuscated_email = email

    html_content = f"""
    <html>
    <p>thanks for signing up</p>
    <a href="http://127.0.0.1:8000/verify_otp?email={email}&otp={otp}">verify email</a>
    </html>
    """
    try:
        setup_yagmail()
        send_email(to_email=email, subject="otp", body=html_content)
        return otp
    except:
        raise HTTPException(status_code=400, detail=str("most likely a network error when sending the email"))


