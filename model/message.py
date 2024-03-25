from base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Message(Base):
    __tablename__ = "message"
    message_id = Column(Integer, autoincrement=True, primary_key=True)
    writer = Column(String(255), nullable=False)


    ForeignKey('fk_message_writer', writer,)