from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    password: str
    email: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
