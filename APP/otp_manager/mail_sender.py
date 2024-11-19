import os
from dotenv import load_dotenv
import yagmail

def setup_yagmail():
    load_dotenv()
    email = "victorfolorunsoofficial@gmail.com"
    app_password = os.getenv("GMAIL_APP_PASSWORD")
    yagmail.register(email, app_password)

def send_email(to_email: str, subject: str, body: str):
    yag = yagmail.SMTP('victorfolorunsoofficial@gmail.com')
    yag.send(
        to=to_email,
        subject=subject,
        contents=body,
        headers={"from": "login project"},
    )
