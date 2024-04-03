import bcrypt


# def hash_password(plain_password: str)->bytes:
#     byted_password = bytes(plain_password, encoding='utf8')
#     salt = bcrypt.gensalt()
#     return bcrypt.hashpw(byted_password, salt)
from customlog import custom_logger
import base64


def verify_password(plain_password, hashed_password: bytes, salt) -> bool:
    # hashed_password = base64.b64decode(hashed_password)
    val = bcrypt.hashpw(bytes(plain_password, encoding='utf8'), salt=salt)
    val = base64.b64encode(val).decode('ascii')
    return val== hashed_password