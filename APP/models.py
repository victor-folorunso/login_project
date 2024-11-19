from pydantic import BaseModel, EmailStr

class User_Detail_Model(BaseModel):
    email: EmailStr
    password: str

class Verify_Otp_Model(BaseModel):
    email: EmailStr
    otp: str