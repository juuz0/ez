from typing import Union, Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schema.schema import ResUser, User, Login, Token
from db.models import UserModal
from db import db
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from pydantic import BaseModel

router = APIRouter()

session = db.SessionLocal()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/signup", response_model=ResUser, status_code=201)
async def signup(user: User):
    safe_pwd = user.password # TODO hashed password

    new_user = UserModal(
        username=user.username,
        password=safe_pwd,
        role=user.role
    )

    db_item = session.query(UserModal).filter(UserModal.username == new_user.username).first()
    if (db_item is not None):
        raise HTTPException(400, detail="a user with this username already exists " + new_user.username)

    session.add(new_user)
    session.commit()
    return new_user


@router.post("/login")
async def login(user: Login):
    db_item = session.query(UserModal).filter(UserModal.username == user.username).first()
    if not db_item:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    final_username: str
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        final_username = username
    except JWTError:
        raise credentials_exception
    user = session.query(UserModal).filter(UserModal.username == final_username).first()
    if user is None:
        raise credentials_exception
    return user


@router.get("/me/")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return {"me": current_user.username}