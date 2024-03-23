from fastapi import FastAPI
import uvicorn
# from config import config
from fastapi import WebSocket, APIRouter, Query, WebSocketException, status, Depends
from dataclasses import dataclass
from typing import ClassVar, Annotated
from utils.token import validate_token
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, DeclarativeBase
from redis import Redis
engine = create_engine("postgresql://test:password@localhost:5432/auth")

# async def getSession():
#     db = Session(engine)
#     try:
#         yield db
#     finally:
#         db.close()

app = FastAPI()

# intersect -- выводит только те строки которые совпадают.
# корреляция
# where exists (подзапрос котторый должен быть связан с таблицей)
# @dataclass
# class 


class ErrorChecker:
    def __call__(self, token: Annotated[str |None, Query] = None):
        if not token:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
        return 'hello'
    

error = ErrorChecker()
@dataclass
class ChatRoom:
    list_conn: ClassVar[list[WebSocket]] = list()

    
    def app_conn(self, ws: WebSocket):
        self.list_conn.append(ws)

    async def broad_cast(self, message):
        for conn in self.list_conn:
            await conn.send_text(message)

    

chat = ChatRoom()

@app.websocket('/ws/{chatroom}')
async def spread_info_into_chat(ws: WebSocket, chatroom: str, username: str = Depends(error)):
    await ws.accept()
    chat.app_conn(ws)
    while True:
        data = await ws.receive_text()
        await chat.broad_cast(username+data)
# 
# app.include_router()
        
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))

    def __repr__(self):
        return f"{self.id}, {self.name}"


if __name__ == "__main__":
    r = Redis()
    r.set('adsf', 'vl')
    r.expire('adsf', 15)
    # config.load_config('conf.ini')
    # uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, log_level='debug')
    # with Session(engine) as db:
    #     u = User(id=44, name='ew')
    #     # db.add(u)
    #     # db.commit()
    #     all = db.query(User).all()
    #     for row in all:
    #         print(row)




# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from fastapi.responses import RedirectResponse, Response
# import jwt
# from data import User
# import uvicorn
# import os
# # from passlib.context import CryptContext
# import bcrypt
# from datetime import timedelta, datetime, timezone
# from redis import Redis


# from fake_view import get_user, add_user, fake_db


# BASE_ACCESS_EXP = 15
# REFRESH_TOKEN_EXP = 90
# secret = '16c6d312d32e872199de59db52d2cc0d473a29d71231314b28feaeabace7ea3b'
# algh_enc = 'HS256'
# black_list = Redis()


# app = FastAPI()
# basic_auth = OAuth2PasswordBearer(
#     tokenUrl='token',
#     auto_error=False,
#     scopes={'chats': 'whatch chat`s'}
# )
    

# @app.get('/res')
# def get_resourse(user: User| None = Depends(validate_token)):
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail='access token expired',
#         )
#     return 'Hello'


# @app.post('/login')
# def login_user(form: OAuth2PasswordRequestForm = Depends()):
#     '''provide access and refresh for user in database'''

#     username = form.username
#     password = form.password
#     if not (user := get_user(username)):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
#                              detail='wrong login or password')
#     if not verify_password(password, user.password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail='wrong login or password')
#     access_exp, refresh_exp = get_exp()
#     data = dict()
#     data['sub'] = username
#     access_token = generate_token(data, access_exp)
#     refresh_token = generate_token(data, refresh_exp)
#     return {'access_token': access_token, 'refresh_token': refresh_token}
    

# @app.post('/refresh')
# def get_access_token(token: Refresh_Token):
#     refresh_token = token.refresh_token
#     payload = get_payload(refresh_token)
#     access_exp, _ = get_exp()
#     data = dict()
#     data['sub'] = payload['sub']
#     return {'access_token': generate_token(data, access_exp)}
    

# @app.logout('/logout')
# def logout(token):
#     '''посмотреть все связанные access token
#     отзывать токены с помощью celery
#     '''

# @app.post('/register')
# def register(form: OAuth2PasswordRequestForm = Depends(), user = Depends(validate_token)):
#     if user:
#         return RedirectResponse('http://localhost:8000/res')
#     username = form.username
#     password = form.password
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(bytes(password, encoding='utf8'), salt)
#     add_user(username, hashed_password)
#     return Response()


# @app.post('/token')
# def create_token(form: OAuth2PasswordRequestForm = Depends()):
#     username = form.username
#     password = form.password
#     if not (user := get_user(username)):
#         raise auth_exception
#     hashed_password = user.password
#     if not verify_password(password, hashed_password):
#         raise auth_exception
#     if not (exp := os.getenv('ACCESS_TOKEN_EXP')):
#         exp = BASE_ACCESS_EXP
#     data = dict()
#     data["sub"]=username
#     return generate_access_token(data, exp)

