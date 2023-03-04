from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime


class ContactModel(BaseModel):
    first_name: str = Field("John", min_length=1, max_length=25)
    last_name: str = Field("Cena", min_length=1, max_length=40)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)
    phone: int = Field("777", gt=100, le=999999999)
    birthday: date


class UpdateContactRoleModel(BaseModel):
    roles: str = Field("'user', 'moderator' or 'admin'")


class ContactDb(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class ResponseContact(BaseModel):
    contact: ContactDb
    detail: str = "User was created successfully"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
