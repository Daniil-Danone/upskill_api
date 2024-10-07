from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr
from config.instance import MALE, FEMALE, DEFAULT


class SexEnum(str, Enum):
    male = MALE
    female = FEMALE
    default = DEFAULT

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str
    birth_date: Optional[str] = None
    sex: SexEnum = SexEnum.default


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreateDB(BaseModel):
    email: str
    password: str
    name: str
    surname: str
    birth_date: Optional[str] = None
    sex: str


class Token(BaseModel):
    user_id: int
    access_token: str
    refresh_token: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    birth_date: Optional[str] = None
    sex: Optional[SexEnum] = None
    phone: Optional[str] = None
    city: Optional[str] = None
