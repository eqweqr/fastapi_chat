import jwt
from typing import List
from customlog import custom_logger
from datetime import datetime, timezone, timedelta
from taskes import redis_message
# just drop token invalid
# raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            #                     detail='Token is invalid',
            #                     headers={'WWW-Authenticate': 'Bearer'},
            #                     )

ALGH = 'HS256'
SECRET = '7a4ab0176241f71dff2226a19aac6fd7d58f36d834d6a4b491fb7f5bcbed202ed8735ef683108531bd6173be309052f7e38d087913c04bbc6323beaed0e73f33'


def get_payload(token: str, secret: str, algorithms: List[str]) -> dict| None:
    try:
        payload = jwt.decode(token, secret, algorithms)
    except jwt.PyJWTError:
        return None
    return payload


def generate_token(secret: str, algorithms: List[str], data: dict, exp: timedelta) -> str:
    """Simillar function for generation access and refresh token"""
    exp = datetime.now(timezone.utc)+exp
    data.update({'exp': exp})
    token = jwt.encode(data, secret, algorithms)
    return token


def validate_token(secret: str, algorithms: str, token: str, fingerprint)->str| None:
    if not token:
        raise Exception('no token')
    if stored_fingerprint := redis_message.get_token_fingerprint(token):
        str_stored_fingerprint = stored_fingerprint.decode('ascii')
        if str_stored_fingerprint != fingerprint:
            redis_message.delete_refresh_token(token)
            raise Exception('different user')
        payload = get_payload(token, secret, algorithms)
        exp = payload['exp']
        if exp < int(datetime.now(timezone.utc).strftime('%s')):
            raise Exception('expired')
        username = payload['sub']
        return username   
    raise Exception('token doesnt exist')

