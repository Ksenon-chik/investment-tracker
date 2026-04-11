from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
import re

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    email: str
    password: str

    @field_validator("password")
    def validator_password(cls, value):
        if len(value) < 8:
            raise ValueError("Пароль должен быть не менее 8 символов")

        if not re.search(r"[A-Za-z]", value):
            raise ValueError("Пароль должен содержать буквы")

        if not re.search(r"\d", value):
            raise ValueError("Пароль должен содержать цифры")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")

        return value

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str