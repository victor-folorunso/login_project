from pydantic import BaseModel, EmailStr

class User_Detail_Model(BaseModel):
    email: EmailStr
    password: str

class Verify_Email_Model(BaseModel):
    email: EmailStr
    otp: str

class Reset_Password_Model(BaseModel):
    email: EmailStr
    otp: str
    new_password: str