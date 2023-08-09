
from configuration import BOT_CONFIG
from .database import (get_async_session, get_chat)


async def get_supported_lang():
    return BOT_CONFIG.get_supported_languages_message()


async def get_chat_lang(chat_id: int, default_lang: str):
    session = await get_async_session()
    chat = await get_chat(chat_id=chat_id, lang=default_lang, session=session)
    return chat.language


async def set_lang(default_lang: str,
                   lang: str,
                   chat_id: int):
    session = await get_async_session()
    chat = await get_chat(chat_id=chat_id, lang=default_lang, session=session)
    if lang in BOT_CONFIG.SUPPORTED_LANGUAGES_CODES:
        chat.language = lang
        await session.merge(chat)
        await session.commit()
        return BOT_CONFIG.SUCCESSFUL_LANG_SET_MESSAGE.get(chat.language)
    else:
        return BOT_CONFIG.LANGUAGE_NOT_SUPPORTED_MESSAGE.get(chat.language)
