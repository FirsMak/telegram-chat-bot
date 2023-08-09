from aiogram import types
from data import (update_karma_mode,
                  get_karma_all,
                  set_karma_all,
                  get_karma,
                  positive_karma_update,
                  )
from .utils import remove_prefix_command


async def get_karma_all_command(message: types.Message):
    print('get_karma_all_handler')
    chat_id = message.chat.id
    default_lang = message.from_user.language_code
    result = await get_karma_all(chat_id=chat_id,
                                 default_lang=default_lang)
    await message.reply(result)


async def set_karma_all_command(message: types.Message):
    print('set_karma_all_handler')
    chat_id = message.chat.id
    default_lang = message.from_user.language_code
    arg = remove_prefix_command(message.text)
    result = await set_karma_all(arg=arg,
                                 chat_id=chat_id,
                                 default_lang=default_lang)
    await message.reply(result)


async def set_karma_mode_command(message: types.Message):
    print('set_karma_mode_command')
    arg = remove_prefix_command(message.text)
    chat_id = message.chat.id
    default_lang = message.from_user.language_code
    result = await update_karma_mode(chat_id=chat_id,
                                     args=arg,
                                     default_lang=default_lang)
    await message.reply(result)


async def get_karma_command(message: types.Message):
    print('get_karma_command')
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.username
    default_lang = message.from_user.language_code
    result = await get_karma(chat_id=chat_id,
                             user_id=user_id,
                             user_name=user_name,
                             default_lang=default_lang)
    await message.reply(result)


async def positive_karma_update_command(message: types.Message):
    chat_id = message.chat.id
    default_lang = message.from_user.language_code
    print('positive_karma_handler')
    try:
        replied_message = message.reply_to_message
        user_id = replied_message.from_user.id
        user_name = replied_message.from_user.username
        karma_state = await positive_karma_update(chat_id=chat_id,
                                                  user_id=user_id,
                                                  user_name=user_name,
                                                  default_lang=default_lang)
        await message.answer(karma_state)

    except AttributeError as e:
        pass
