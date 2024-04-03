from model.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from model.user import User
from model.chat import Chat


class Message(Base):
    __tablename__ = "message"
    message_id = Column(Integer, autoincrement=True, primary_key=True)
    writer_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(Integer, ForeignKey('chat.chat_id'))
    message = Column(String)
