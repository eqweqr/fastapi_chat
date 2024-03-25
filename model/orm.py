from db import Session
from user import User
from chat import Chat
from sqlalchemy.orm import load_only


def is_valid(email: str) -> bool:
    with Session.begin() as db:
       return db.query(User).filter(User.email==email).options(load_only(User.activated)).one()


def confirm_email(email: str) -> None:
    with Session.begin() as db:
        db.query(User).filter(User.email==email).update({'activated': True})

def add_user(username, hashed_password, email):
    with Session.begin() as db:
        db.add(User(username=username, hashed_password=hashed_password, email=email, activated=False))
            
def get_user(email):
    with Session.begin() as db:
        return db.query(User).filter(User.email==email).first()
    
# def create_chat(ema)