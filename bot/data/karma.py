
from configuration import (
    BOT_CONFIG,
)
from sqlalchemy import select, update
from .database import (get_async_session, get_chat, get_user, User)


async def get_karma_all(chat_id: int, default_lang: str):
    session = await get_async_session()
    chat = await get_chat(chat_id=chat_id, lang=default_lang, session=session)
    if chat.karma_mode:
        get = select(User).where(User.chat_id ==
                                 chat_id).order_by(User.karma.desc())
        result = await session.execute(get)
        users = result.scalars()
        result = ''
        is_zero_members = True
        for i, user in enumerate(users):
            is_zero_members = False
            print(user.karma)
            result += f'{i+1}. @{user.user_name} - {user.karma} \n'
        if is_zero_members:
            return BOT_CONFIG.get_zero_karma_members_message(chat.language,
                                                             BOT_CONFIG.DEFAULT_KARMA_VALUE)
        else:
            return result
    else:
        return BOT_CONFIG.KARMA_MODE_EXCEPTION_MESSAGE.get(chat.language)


async def set_karma_all(chat_id: int,
                        arg: str,
                        default_lang: str
                        ):
    session = await get_async_session()
    chat = await get_chat(chat_id=chat_id, lang=default_lang, session=session)
    try:
        karma = int(arg)
        if chat.karma_mode:
            stmt = update(User).where(User.chat_id ==
                                      chat_id).values(karma=karma)
            await session.execute(stmt)
            await session.commit()
            return BOT_CONFIG.SUCCESS_RESULT_MESSAGE.get(chat.language)
        else:
            return BOT_CONFIG.KARMA_MODE_EXCEPTION_MESSAGE.get(chat.language)
    except ValueError:
        return BOT_CONFIG.ARG_NOT_RECOGNIZED_MESSAGE.get(chat.language)


async def get_karma(chat_id: int,
                    user_id: int,
                    user_name: str,
                    default_lang: str,
                    ):
    session = await get_async_session()
    user = await get_user(user_id=user_id,
                          chat_id=chat_id,
                          user_name=user_name,
                          session=session)
    chat = await get_chat(chat_id=chat_id, lang=default_lang, session=session)
    if chat.karma_mode:
        return BOT_CONFIG.get_karma_state_message(chat.language,
                                                  user.karma)
    else:
        return BOT_CONFIG.KARMA_MODE_EXCEPTION_MESSAGE.get(chat.language)


async def set_karma(user_id: int,
                    chat_id: int,
                    user_name: str,
                    karma: int,
                    default_lang: str,
                    ):
    session = await get_async_session()
    chat = await get_chat(chat_id=chat_id, lang=default_lang, session=session)
    if chat.karma_mode:
        user = await get_user(user_id=user_id,
                              chat_id=chat_id,
                              user_name=user_name,
                              session=session)
        user.karma = karma
        await session.merge(user)
        await session.commit()
        return BOT_CONFIG.get_karma_state_message(chat.language,
                                                  user.karma)
    else:
        return BOT_CONFIG.KARMA_MODE_EXCEPTION_MESSAGE.get(chat.language)


async def positive_karma_update(user_id: int,
                                chat_id: int,
                                user_name: str,
                                default_lang: str
                                ):
    session = await get_async_session()
    chat = await get_chat(chat_id=chat_id, lang=default_lang, session=session)
    if chat.karma_mode:
        user = await get_user(user_id=user_id,
                              chat_id=chat_id,
                              user_name=user_name,
                              session=session)
        user.karma = user.karma + BOT_CONFIG.POSITIVE_KARMA_CHANGE
        await session.merge(user)
        await session.commit()
        return BOT_CONFIG.get_karma_positive_update_message(lang=chat.language,
                                                            user_name=user_name,
                                                            karma_value=user.karma)
    else:
        return BOT_CONFIG.KARMA_MODE_EXCEPTION_MESSAGE.get(chat.language)


async def update_karma_mode(chat_id: int,
                            default_lang: str,
                            args: str,
                            ):
    session = await get_async_session()
    chat = await get_chat(chat_id=chat_id, lang=default_lang, session=session)
    if args == BOT_CONFIG.ON_STATE:
        chat.karma_mode = True
        await session.merge(chat)
        await session.commit()
        return BOT_CONFIG.get_karma_mode_update_message(chat.language,
                                                        chat.karma_mode)
    elif args == BOT_CONFIG.OFF_STATE:
        chat.karma_mode = False
        await session.merge(chat)
        await session.commit()
        return BOT_CONFIG.get_karma_mode_update_message(chat.language,
                                                        chat.karma_mode)
    else:
        return BOT_CONFIG.ARG_NOT_RECOGNIZED_MESSAGE.get(chat.language)
