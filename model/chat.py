from model.base import Base
from model.user import User
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

class Chat(Base):
    __tablename__ = "chat"
    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    chat_name = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
        
    messages = relationship('Message', backref='chat')
