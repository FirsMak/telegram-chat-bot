from sqlalchemy import (Column,
                        BigInteger,
                        String,
                        Boolean)
from .base import Base


class Chat(Base):
    __tablename__ = 'chats'
    chat_id = Column(BigInteger, primary_key=True)
    prefix = Column(String, nullable=False)
    language = Column(String, nullable=False)
    karma_mode = Column(Boolean, nullable=False)
    antiflood = Column(Boolean, nullable=False)
