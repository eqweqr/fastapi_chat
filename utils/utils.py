import bcrypt


def hash_password(plain_password: str)->bytes:
    byted_password = bytes(plain_password, encoding='utf8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(byted_password, salt)


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    val = bcrypt.hashpw(bytes(plain_password, encoding='utf8'), hashed_password)
    print(val)
    return val== hashed_password