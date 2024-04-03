from fastapi import FastAPI, Query, WebSocketException
from sqlmodel import Field, SQLModel
from fastapi.middleware.cors import CORSMiddleware
from middleware.middleware import RouterLoggingMiddleware
from fastapi import APIRouter, Response, status, Depends, Form, Header, Request, Security
from contextlib import asynccontextmanager
from utils.utils import verify_password
from fastapi.security import OAuth2PasswordRequestForm, SecurityScopes, OAuth2PasswordBearer
from fastapi import HTTPException
from utils.token import generate_token, get_payload, validate_token
import bcrypt
from fastapi.exceptions import HTTPException
from data.reg import RegisterForm
from model.db import add_user, get_user, confirm_email, create_chat, get_chats
from typing import Annotated
import uvicorn
from taskes import redis_chats
import base64
from fastapi.websockets import WebSocket
from taskes import redis_message
from taskes.message_cacher import create_new_chat, get_cached_messages, add_message
from typing import List, Dict
from datetime import timedelta, datetime, timezone
from customlog import custom_logger
from taskes.tasks import send_confimation_message
from model.migration import get_alembic_config, run_upgrade, run_downgrade
from fastapi.websockets import WebSocket
import json


basic_auth = OAuth2PasswordBearer(
    tokenUrl='/login',
    scopes={'chat:visit': 'Watch list of available chats', 'chat:edit': 'Creating chats or connecting to available'}
    )


origins = [
    'http://localhost:5173',
]


def make_migrations():
    cfg = get_alembic_config()
    run_upgrade(cfg)
    

app = FastAPI()


app.add_middleware(
    RouterLoggingMiddleware
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

salt = bcrypt.gensalt(14)
ALGH = 'HS256'
SECRET = '7a4ab0176241f71dff2226a19aac6fd7d58f36d834d6a4b491fb7f5bcbed202ed8735ef683108531bd6173be309052f7e38d087913c04bbc6323beaed0e73f33'


def validate_access_token(
        security_scopes: SecurityScopes,
        token = Depends(basic_auth)):
    if security_scopes.scopes:
        authentication_type = f'Bearer scopes="{security_scopes.scope_str}"'
    else:
        authentication_type = 'Bearer'
    if not token:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='coudnt provide access',
            headers={'WWW-Authenticate': authentication_type},
        )
    secret = SECRET
    algorithn = ALGH
    payload = get_payload(token, secret, algorithn)
    exp = payload['exp']
    if exp < int(datetime.now(timezone.utc).strftime('%s')):
        raise Exception('expired')
    
    user_scopes = payload['scopes']
    custom_logger.info(user_scopes)
    for scope in security_scopes.scopes:
        if scope not in user_scopes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='no permission',
                headers={'WWW-Authenticate': authentication_type},
            )
            
    username = payload['sub']
    
    return username   
    

@app.post('/validate')
def validate_for_frontend(username: str = Depends(validate_access_token)):
    custom_logger.info(username)
    return {'username': username}

@app.post('/register')
def register(username: Annotated[str, Form()], 
             email: Annotated[str, Form()],
             password: Annotated[str, Form()]):# user = Depends(validate_token)):
    hashed_password = bcrypt.hashpw(bytes(password, encoding='utf8'), salt)
    encrypted = base64.b64encode(hashed_password).decode('ascii')
    custom_logger.info(encrypted)
    try:
        add_user(username=username, hashed_password=encrypted,
             email=email)
    except Exception as exp:
        custom_logger.info(exp)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                      detail='There are user with same email')
    hashed_username = bcrypt.hashpw(bytes(username, encoding='utf8'), salt=salt)
    str_hashed_username = base64.b64encode(hashed_username).decode('ascii')
    # send_confimation_message.delay(email, str_hashed_username)
    custom_logger.info(str_hashed_username)
    return Response(status_code=status.HTTP_201_CREATED) 


@app.post('/login')
def login_user(user_agent: Annotated[str| None, Header()],
               request: Request,
               form: OAuth2PasswordRequestForm = Depends(),
            ):
    '''provide access and refresh for user in database'''
    custom_logger.info(form.username)
    username = form.username
    password = form.password
    ip = request.client.host
    value_for_token = ip+user_agent
    if not (user := get_user(username)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                             detail='wrong login or password',
                             headers={"WWW-Authenticate": "Bearer"}
                             )
    user_scopes = None
    custom_logger.info('ok' if user.activated else 'err')
    if user.activated:
        user_scopes = ['chat:visit', 'chat:edit']
    else:
        user_scopes = ['chat:visit']
    if not verify_password(password, user.hashed_password, salt):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                             detail='wrong login or password',
                             headers={"WWW-Authenticate": "Bearer"}
                             )
    access_exp, refresh_exp = timedelta(minutes=15), timedelta(minutes=90)
    data = dict()
    data['sub'] = username
    data['scopes'] = user_scopes
    access_token = generate_token(SECRET, ALGH, data, access_exp)
    refresh_token = generate_token(SECRET, ALGH, data, refresh_exp)
    redis_message.add_refresh_token(refresh_token, value_for_token, 90*60)
    return {'access_token': access_token, 'refresh_token': refresh_token}


@app.post('/refresh', status_code=status.HTTP_200_OK)
def get_access_token(grant_type: Annotated[str, Form()],
                        refresh_token: Annotated[str, Form()],
                        user_agent: Annotated[str| None, Header()],
                        request: Request):
    ip = request.client.host
    value_for_token = ip+user_agent
    if not grant_type == 'refresh_token':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                             detail='different grant type')
    else:
        custom_logger.info(refresh_token)
        username = None
        try:
            username = validate_token(SECRET, ALGH, refresh_token, value_for_token)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=e.args,
                                headers={"WWW-Authenticate": "Bearer"}
                                )
        user_scopes = get_payload(refresh_token, SECRET, [ALGH])['scopes']
        access_exp = timedelta(minutes=15)
        data = dict()
        data['sub'] = username
        data['scopes'] = user_scopes
        return {'username': username, 'access_token': generate_token(SECRET, ALGH, data, access_exp)}
        

@app.post('/logout')
def logout(grant_type: Annotated[str, Form()],
            refresh_token: Annotated[str, Form()]):
    if grant_type == 'refresh_token':
        redis_message.delete_refresh_token(refresh_token)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Wrong auth type')


@app.get('/')
def hel(username = Security(validate_access_token, scopes=['chat:visit'])):
    return username


@app.get('/no')
def hel(username=Security(validate_access_token, scopes=['chat:edit'])):
    return 'hi'


@app.patch('/confirm/{username}')
def confirm_email_req(username: str, hashed: str = Query()):
    hashed_username = bcrypt.hashpw(bytes(username, encoding='utf8'), salt=salt)
    str_hashed_username = base64.b64encode(hashed_username).decode('ascii')
    custom_logger.info(str(hashed).strip() == str_hashed_username.strip())
    custom_logger.info(str(hashed).strip())
    custom_logger.info(str_hashed_username.strip())
    if str(hashed).strip() == str_hashed_username.strip():
        confirm_email(username) # delay task
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='there isnt user with this signature'
                        )


@app.post('/chat/new')
def create_new_chatr(username = Security(validate_access_token, scopes=['chat:visit', 'chat:edit']), chatname = Form(), password = Form()):
    hashed_password = bcrypt.hashpw(bytes(password, encoding='utf8'), salt=salt)
    str_hashed_password = base64.b64encode(hashed_password).decode('ascii')
    try:
        id_chat = create_chat(chatname, username, str_hashed_password)
        chat.create_new_chatroom(chat_id=id_chat)
        custom_logger.info(chat.list_conn)
    except Exception as exp:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=exp)
    create_new_chat(id_chat)
    return id_chat


@app.get('/chat/get')
def get_awailable_chats(username = Security(validate_access_token, scopes=['chat:visit']), limit: int| None= Query(), page: int| None = Query()):
    chats = get_chats(limit=limit, offset=page)
    wrapped_chats = []
    for chat in chats:
        wrapped_chats.append({'owner': chat[0], 'room': chat[1], 'id': chat[2]})
    return wrapped_chats


def validate_websocket_token(token: str| None = None):
    if not token:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason='no user token provided'
        )
    secret = SECRET
    algorithn = ALGH
    payload = get_payload(token, secret, algorithn)
    exp = payload['exp']
    if exp < int(datetime.now(timezone.utc).strftime('%s')):
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason='no user token provided'
        )
    username = payload['sub']
    return username   
    

class ChatRoom:
    list_conn: Dict[int, List[WebSocket]]

    def __init__(self):
        self.list_conn = dict()

    def create_new_chatroom(self, chat_id):
        self.list_conn[chat_id]=[]

    def delete_conn(self, chat_id, ws):
        ws.close()
        self.list_conn[chat_id].remove(ws)


    async def connect_to_chat(self, chat_id: int, ws: WebSocket):
        chat_id = int(chat_id)
        for i in self.list_conn.keys():
            custom_logger.info(i)
        # custom_logger.insfo(self.list_conn.keys())
        if chat_id not in self.list_conn.keys():
            raise 'chat doesnt exist'
        await ws.accept()
        self.list_conn[chat_id].append(ws)

    async def broad_cast(self, chat_name, message):
        for conn in self.list_conn[chat_name]:
            await conn.send_text(message)


@app.get('/ws/getMessages/{id_room}')
def get_messages_from_chat(id_room):#, username = Security(validate_access_token, scopes=['chat:visit', 'chat:edit'])):
    messages = get_cached_messages(id_room)
    message_list = []
    custom_logger.info(messages)
    for message in messages:
        auth, mes = message.decode('ascii').split('zxcqwe')
        val = {'message': mes, 'username': auth}
        message_list.append(val)
    custom_logger.info(chat.list_conn)
    return message_list


@app.websocket('/ws/{chatroom}')
async def write_message(ws: WebSocket, chatroom: str, 
                        token):
    try:
        custom_logger.info(ws)
        username=validate_websocket_token(token) 
        await chat.connect_to_chat(chatroom, ws)
        while True:
            message = await ws.receive_text()
            
            add_message(chatroom, message, username)
            data = {
                'message': message,
                'username': username
            }
            json_message = json.dumps(data)

            await chat.broad_cast(int(chatroom),json_message)
    except:
        chat.delete_conn(chatroom, ws)
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason='no user token provided'
        )

chat = ChatRoom()


if __name__ == "__main__":
    make_migrations()
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
