
from configuration import BOT_CONFIG
from .database import (get_async_session, get_chat)


async def get_antiflood(chat_id: int, default_lang: str):
    session = await get_async_session()
    chat = await get_chat(chat_id=chat_id, lang=default_lang, session=session)
    if chat.antiflood is None:
        return True
    else:
        return chat.antiflood


async def set_antiflood(chat_id: int,
                        default_lang: str,
                        arg: str):
    session = await get_async_session()
    chat = await get_chat(chat_id=chat_id, lang=default_lang, session=session)
    if arg == BOT_CONFIG.ON_STATE:
        chat.antiflood = True
        await session.merge(chat)
        await session.commit()
        return BOT_CONFIG.SUCCESS_RESULT_MESSAGE.get(chat.language)
    elif arg == BOT_CONFIG.OFF_STATE:
        chat.antiflood = False
        await session.merge(chat)
        await session.commit()
        return BOT_CONFIG.SUCCESS_RESULT_MESSAGE.get(chat.language)
    else:
        return BOT_CONFIG.ARG_NOT_RECOGNIZED_MESSAGE.get(chat.language)
