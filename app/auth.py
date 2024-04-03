from fastapi import APIRouter, Response, status, Depends
from utils.utils import hash_password, verify_password
from fastapi.security import OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer
from fastapi import HTTPException
from utils.token import generate_token, get_payload
from utils.token import validate_token
import bcrypt
from fastapi.exceptions import HTTPException
from data.reg import RegisterForm
from model.db import add_user
from taskes.tasks import send_confimation_message

basic_auth = OAuth2PasswordBearer(tokenUrl='/auth/token')
auth = APIRouter(prefix='/auth')


@auth.post('/register')
def register(form: RegisterForm = Depends()):# user = Depends(validate_token)):
    username = form.username
    password = form.password
    email = form.email
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes(password, encoding='utf8'), salt)
    try:
        add_user(username=username, hashed_password=hashed_password,
             email=email)
    except Exception:
        HTTPException(status_code=status.HTTP_409_CONFLICT,
                      details='There are user with same email')
    send_confimation_message.delay(email)
    return Response(status_code=status.HTTP_201_CREATED) 







# @auth.post('/login')
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
#     access_exp, refresh_exp = 15, 90
#     data = dict()
#     data['sub'] = username
#     access_token = generate_token(data, access_exp)
#     refresh_token = generate_token(data, refresh_exp)
#     return {'access_token': access_token, 'refresh_token': refresh_token}




# @auth.patch('/confirm')
# def confirm(email: str):
#     user = get_user_by_email(email)
#     if user.isActive():
#         return Response(status_code=status.HTTP_202_ACCEPTED)

# @auth.post('/login')
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
#     access_exp, refresh_exp = 15, 90
#     data = dict()
#     data['sub'] = username
#     access_token = generate_token(data, access_exp)
#     refresh_token = generate_token(data, refresh_exp)
#     return {'access_token': access_token, 'refresh_token': refresh_token}
    

# @auth.post('/refresh')
# def get_access_token(token: Refresh_Token):
#     refresh_token = token.refresh_token
#     payload = get_payload(refresh_token)
#     access_exp, _ = get_exp()
#     data = dict()
#     data['sub'] = payload['sub']
#     return {'access_token': generate_token(data, access_exp)}
    

# @auth.logout('/logout')
# def logout(token):
#     '''посмотреть все связанные access token
#     отзывать токены с помощью celery
#     '''


# @auth.post('/token')
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
