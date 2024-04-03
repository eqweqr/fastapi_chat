from sqlalchemy import insert, create_engine, select
from sqlalchemy.orm import sessionmaker, scoped_session, load_only, Session
from model.user import User
from model.chat import Chat
from model.message import Message
from customlog import custom_logger
import copy
from typing import Tuple
from contextlib import contextmanager


engine = create_engine('postgresql://test:password@localhost/start_alembic')
session_factory = sessionmaker(bind=engine, expire_on_commit=False)
# Session = scoped_session(session_factory=session_factory)
# se = session_factory()

# def dbconnect(func):
#     # decorator for orm func
#     def wrapper(*args, **kwargs):
#         val=None
#         session = Session()
#         try:
#             val = copy.deepcopy(func(*args, **kwargs))
#             print('val', val)
#             session.commit()
#         except:
#             session.rollback()
#             raise
#         finally:
#             Session.remove()
#         return val
#     return wrapper

@contextmanager
def atomic_session(func_name: str =None):
    session = session_factory()
    try:
        custom_logger.info('Start transaction: {0}'.format(func_name))
        yield session
        session.commit()
        custom_logger.info('Successful transaction')
    except:
        custom_logger.error('Transaction rollback')
        session.rollback()
        raise    
    finally:
        session.close()


def is_user_confirmed(username: str) -> bool:
    with atomic_session('is_user_confirmed') as session:
        query = select(User.activated).filter_by(username=username)
        return session.execute(query).fetchone()[0]


def confirm_email(username: str) -> bool:
    with atomic_session('confirm_email') as session:
        session.query(User).filter_by(username=username).update({'activated': True})


def get_chats(*, limit=None, offset=None):
    with atomic_session('get_chats') as session:
        query = select(User.username, Chat.chat_name, Chat.chat_id).join(User.chats)
        if limit: 
            query = query.limit(limit)
        if offset:
            query = query.offset(offset*limit)
        return session.execute(query).fetchall()

def get_user_messages_in_chat(username):
    with atomic_session('get_user_messages_in_chat') as session:
        query = select(User.username, Chat.chat_name).join(User.chats).where(User.username==username)
        return session.execute(query).fetchall()


def get_messages_from_chat(chat_name, *, limit=None, offset=None):
    with atomic_session('get_messages_from_chatfunc_name') as session:
        query = select(User.username, Message.message).join(User.chats).join(Chat.messages).where(Chat.chat_name==chat_name)
        if limit:
            query=query.limit(limit)
        if offset:
            query=query.offset(offset)
        return session.execute(query).fetchall()


def create_message(chat_name, username, message):
    with atomic_session('create_message') as session:
        query = select(User.id).filter_by(username=username)
        user_id=session.execute(query).fetchone()
        query = select(Chat.chat_id).filter_by(chat_name=chat_name)
        chat_id=session.execute(query).fetchone()
        session.add(Message(writer_id=user_id[0], chat_id=chat_id[0], message=message))


def create_chat(chat_name, owner, hashed_password):
    with atomic_session('create_chat') as session:
        query = select(User.id).filter_by(username=owner)
        user_id=session.execute(query).fetchone()
        id = user_id[0]
        custom_logger.info(id)
        query = insert(Chat).values([{'chat_name': chat_name, 'owner_id': id, 'hashed_password': hashed_password}]).returning(Chat.chat_id)
        chat_ids = session.execute(query).one()
        chat_id = []
        for id in chat_ids:
            return id

        # return chat_id[0]

def add_user(username, hashed_password, email):
    with atomic_session('add_user') as session:
        session.add(User(username=username, hashed_password=hashed_password, email=email, activated=False))


def get_user(username: str):
    with atomic_session('get_users') as session:
        return session.query(User).filter(User.username==username).one()
    

# chats = get_chats(limit=10)
# wrapped_chats = []
# for chat in chats:
#     wrapped_chats.append({chat[0]: chat[1]})
# print(wrapped_chats)