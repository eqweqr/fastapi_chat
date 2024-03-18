from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from pydentic import Base
import jwt
from data import User
import os
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone


from fake_view import get_user

BASE_ACCESS_EXP = 15
secret = '16c6d312d32e872199de59db52d2cc0d473a29d71231314b28feaeabace7ea3b'
algh_enc = 'HS256'
cc = CryptContext(schemes=['bcrypt'], depricated='auto')



# basic_auth -- будет анализировать request, будет смотреть authentication header
app = FastAPI('/auth')
basic_auth = OAuth2PasswordBearer(
    tokenUrl='token',
    scopes={'chats': 'whatch chat`s'}
)

auth_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail = 'provide wrong password or login',
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pass
    # cc.verify(plain_password, hashed_password)


def generate_access_token(data: dict, exp: timedelta = timedelta(minutes=15)) -> str:
    pass


def get_payload(token: str):
    try:
        payload = jwt.decode(token, secret, algorithms=[algh_enc])
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='can`t decode jwt token')
    return payload


def validate_token(token: str = Depends(basic_auth))->User:
    payload = get_payload(token)
    exp = payload['exp']
    username = payload['sub']
    if datetime(exp) < datetime.now(timezone.utc):
        return None
    if userget_user(username)
    return True


@app.get('/res')
def get_resourse(authenticated: bool = Depends(validate_token)):
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='access token expired',
        )
    return 'Hello'


@app.post('/token')
def create_token(form: OAuth2PasswordRequestForm):
    username = form.username
    password = form.password
    if not (user := get_user(username)):
        raise auth_exception
    hashed_password = user.password
    if not verify_password(password, hashed_password):
        raise auth_exception
    if not (exp := os.getenv('ACCESS_TOKEN_EXP')):
        exp = BASE_ACCESS_EXP
    data = dict()
    data["sub"]=username
    return generate_access_token(data, exp)

