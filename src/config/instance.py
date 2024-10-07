import os
from dotenv import load_dotenv

load_dotenv()

# PostreSQL
POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")

# Users
## SEX
MALE: str = "male"
FEMALE: str = "female"
DEFAULT: str = "default"

## ROLE
STUDENT: str = "student"
TEACHER: str = "teacher"
ADMIN: str = "admin"

# TOKEN
TOKEN_TYPE: str = "Bearer"
JWT_ALGORITHM: str = "HS256"
JWT_SECRET: str = os.environ.get("JWT_SECRET")

ACCESS_TOKEN_LIFETIME: int = 30
REFRESH_TOKEN_LIFETIME: int = 60

