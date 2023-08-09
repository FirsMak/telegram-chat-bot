from data import set_antiflood
from aiogram import types
from .utils import remove_prefix_command


async def set_antiflood_command(message: types.Message):

    chat_id = message.chat.id
    default_lang = message.from_user.language_code
    arg = remove_prefix_command(message.text)
    print(f'args {arg}')
    result = await set_antiflood(chat_id=chat_id,
                                 default_lang=default_lang,
                                 arg=arg)
    await message.reply(result)
