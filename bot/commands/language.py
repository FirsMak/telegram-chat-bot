from aiogram import types
from data import get_supported_lang, set_lang
from .utils import remove_prefix_command


async def set_lang_command(message: types.Message):
    print('set_language_handler')
    chat_id = message.chat.id
    default_lang = message.from_user.language_code
    arg = remove_prefix_command(message.text)
    result = await set_lang(lang=arg,
                            chat_id=chat_id,
                            default_lang=default_lang)
    await message.reply(result)


async def get_supported_lang_command(message: types.Message):
    print('get_languages_handler')

    result = await get_supported_lang()
    await message.reply(result)
