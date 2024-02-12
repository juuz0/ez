from pydantic import BaseModel
from typing import Optional
from enum import Enum
from dataclasses import dataclass
from sqlalchemy import LargeBinary

class Role(str,Enum):
    CLIENT = "client"
    OPS = "ops"

@dataclass
class SignUser:
    username: str
    password: str
    role: Role


class User(BaseModel):
    username: str
    password: str
    role: Role

    class Config:
        orm_mode = True

class ResUser(BaseModel):
    username: str
    role: Role

    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str