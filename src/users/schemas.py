from enum import Enum
from typing import Dict, Optional
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
    birthDate: Optional[str] = None
    sex: SexEnum = SexEnum.default


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreateDB(BaseModel):
    email: str
    password: str
    name: str
    surname: str
    birthDate: Optional[str] = None
    sex: str


class UserDump(BaseModel):
    id: int
    email: str
    role: str
    name: str
    surname: str
    birthDate: Optional[str] = None
    sex: str
    phone: Optional[str] = None
    city: Optional[str] = None
    createdAt: str


class Token(BaseModel):
    user: UserDump
    access_token: str
    refresh_token: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    birthDate: Optional[str] = None
    sex: Optional[SexEnum] = None
    phone: Optional[str] = None
    city: Optional[str] = None
