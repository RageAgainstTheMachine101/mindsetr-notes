from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str

class UserUpdate(BaseModel):
    username: str

class UserResponse(BaseModel):
    email: EmailStr
    username: str
