from sqlalchemy import (Column,
                        Integer,
                        BigInteger,
                        String)
from .base import Base


class StopWord(Base):
    __tablename__ = "stop_words"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, nullable=False)
    word = Column(String, nullable=False)
