from model.base import Base
import re
from dataclasses import dataclass
from sqlalchemy.orm import validates, relationship, load_only, sessionmaker
from sqlalchemy import Integer, Column, String, Boolean, ForeignKey, create_engine

engine = create_engine('postgresql://test:password@localhost/start_alembic')
Session = sessionmaker(engine)
EMAIL_PATTERN = r'^([A-Za-z0-9]*[.-_]*[A-Za-z0-9]*)+@[A-Za-z]*(\.[A-z|a-z]{2,})*$'
REGEX_EMAIL = re.compile(EMAIL_PATTERN)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True)
    hashed_password = Column(String(255))
    email = Column(String(255), unique=True)
    activated = Column(Boolean, default=False)    
    chats = relationship('Chat', backref='users')
    messages = relationship('Message', backref='users')

    @validates('email')
    def validate_email(self, key, email):
        if not re.fullmatch(REGEX_EMAIL, email):
            raise ValueError('incorrect email format')
        return email

    def __repr__(self) -> str:
        return "User(%s, %s)" % (self.username, self.email)