from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: str = "participant"


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
