
from configuration import BOT_CONFIG
from .database import (get_async_session, get_chat, StopWord)

from sqlalchemy import and_, select, delete


async def delete_stop_words(chat_id: int,
                            default_lang: str,
                            words: list[str]):
    session = await get_async_session()
    chat = await get_chat(chat_id, session)
    stmt = delete(StopWord).where(
        and_(StopWord.chat_id == chat_id, StopWord.word.in_(words)))
    await session.execute(stmt)
    return BOT_CONFIG.SUCCESS_RESULT_MESSAGE.get(chat.language)


async def get_stop_words(chat_id: int, default_lang: str):
    session = await get_async_session()
    chat = await get_chat(chat_id=chat_id, lang=default_lang, session=session)
    get = select(StopWord).where(StopWord.chat_id == chat_id)
    result = await session.execute(get)
    words = result.fetchall()
    if len(words) == 0:
        return BOT_CONFIG.STOP_WORDS_NOT_FOUND_MESSAGE.get(chat.language)
    else:
        return BOT_CONFIG.get_stop_word_list_message(words)


async def add_stop_words(chat_id: int,
                         default_lang: str,
                         words: list[str]):
    session = await get_async_session()
    chat = await get_chat(chat_id=chat_id, lang=default_lang, session=session)
    new_words = []
    for word in words:
        new_words.append(StopWord(chat_id=chat_id, word=word))

    session.add_all(new_words)
    session.commit()
    return BOT_CONFIG.SUCCESSFUL_ADD_STOP_WORDS_MESSAGE.get(chat.language)
