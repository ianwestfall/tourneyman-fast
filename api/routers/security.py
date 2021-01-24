from datetime import timedelta, datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api import schemas
from api.schemas.security import Token, TokenData
from database.db import get_db
from database.models import User
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

router = APIRouter()


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oath2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')
oath2_scheme_allow_anonymous = OAuth2PasswordBearer(tokenUrl='/auth/token', auto_error=False)


def verify_password(plaintext, hashed):
    return pwd_context.verify(plaintext, hashed)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post('/users/', response_model=schemas.security.User)
def create_user(user: schemas.security.UserCreate, db: Session = Depends(get_db)):
    db_user = User.by_email(user.email, db)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    # Overwrite user.password with a hashed version
    user.password = get_password_hash(user.password)
    return User.create(user, db)


# noinspection PyTypeChecker
@router.get('/users/', response_model=List[schemas.security.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return User.get_all(db, skip, limit)


def get_user(db, email: str):
    user = User.by_email(email, db)
    return user


def authenticate_user(db, email: str, password: str) -> Optional[User]:
    user = get_user(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oath2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_or_none(token: str = Depends(oath2_scheme_allow_anonymous), db: Session = Depends(get_db)):
    if token:
        return await get_current_user(token, db)
    else:
        return None


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Inactive user')
    return current_user


async def get_current_active_user_or_none(current_user: User = Depends(get_current_user_or_none)):
    if current_user:
        return await get_current_active_user(current_user=current_user)
    return None


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}
