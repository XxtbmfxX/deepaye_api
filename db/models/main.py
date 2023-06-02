from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    email: str
    disabled: bool or None = None


class UserInDb(User):
    hashed_password: Optional[str]


class Token(BaseModel):
    acces_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None = None
