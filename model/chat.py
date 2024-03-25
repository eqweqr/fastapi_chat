from base import Base
from user import User
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

class Chat(Base):
    __tablename__ = "chat"
    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    chat_name = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    owner_id = Column(Integer, ForeignKey(User.id))
    owner = relationship(User)