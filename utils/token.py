import jwt
from typing import List
from datetime import datetime, timezone, timedelta
# just drop token invalid
# raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            #                     detail='Token is invalid',
            #                     headers={'WWW-Authenticate': 'Bearer'},
            #                     )
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


def validate_token(token)->str| None:
    if not token:
        return None
    payload = get_payload(token)
    exp = payload['exp']
    if exp < int(datetime.now(timezone.utc).strftime('%s')):
        return None
    username = payload['sub']
    return get_user(username)