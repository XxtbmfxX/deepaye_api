from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db.schemas.user import user_schema
from db.models.main import User, UserInDb, TokenData, Token

from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from db.client import db_client


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 3
SECRET = "7cf59788ab1345df8e820c24651bb867ab44a507448eb8bbf50b7f0bd8472366"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# matches the url to do the login
oauth2 = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter(prefix="/jwtauth",
                   tags=["jwtauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


# create functions to verify password, get password hash, get user, authenticate_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    user = user_schema(db_client.users.find_one({"username": username}))
    if user:
        return UserInDb(**user)  # returns all except the password


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    # defined in models
    if not verify_password(password, user["hashed_password"]):
        return False

    return user


def create_acces_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


# get current user from token
async def get_current_user(token: str = Depends(oauth2)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# get active user


async def get_current_active_user(current_user: UserInDb = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get("/token", response_model=Token)
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"},
                            )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = create_acces_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token,  "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: UserInDb = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
