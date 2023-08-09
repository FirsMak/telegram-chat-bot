from sqlalchemy import (Column,
                        Integer,
                        BigInteger,
                        String)
from .base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    chat_id = Column(BigInteger, nullable=False)
    user_name = Column(String, nullable=False)
    karma = Column(Integer, nullable=False)
