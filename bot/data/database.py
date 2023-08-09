from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, select

from db import (User, Chat, StopWord)
from configuration import (POSTGRES_USER,
                           POSTGRES_PASS,
                           POSTGRES_HOST,
                           BOT_CONFIG,
                           )
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}?async_fallback=True"

Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)


async def get_async_session():
    async with async_session_maker() as session:
        async with session.begin():
            session: AsyncSession
        return session


async def get_user(user_id: int,
                   chat_id: int,
                   user_name: str,
                   session: AsyncSession):

    get = select(User).where(
        and_(User.user_id == user_id, User.chat_id == chat_id))
    result = await session.execute(get)
    user = result.scalar_one_or_none()
    if user is None:
        return User(user_id=user_id,
                    chat_id=chat_id,
                    user_name=user_name,
                    karma=BOT_CONFIG.DEFAULT_KARMA_VALUE)
    else:
        return user


async def get_chat(chat_id: int,
                   session: AsyncSession,
                   lang: str = BOT_CONFIG.DEFAULT_LANG):
    get = select(Chat).where(Chat.chat_id == chat_id)
    result = await session.execute(get)
    chat = result.scalar_one_or_none()
    if chat is None:
        return Chat(chat_id=chat_id,
                    prefix=BOT_CONFIG.DEFAULT_PREFIX,
                    language=lang,
                    karma_mode=BOT_CONFIG.DEFAULT_KARMA_MODE,
                    antiflood=BOT_CONFIG.DEFAULT_ANTIFLOOD)
    else:
        return chat
