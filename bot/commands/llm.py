from aiogram import Bot, types
from converter import Converter
from configuration import (Message, BOT_CONFIG)
import os
from .utils import remove_prefix_command
from data import (get_prefix, set_prefix, get_chat_lang, generate_response)


prefixes = ["/сара ", '/sara ']
voice_prefixes = ["сара ", 'сара, ']


def remove_prefix(s, prefix):
    return s[len(prefix):]


async def get_prefix_command(message: types.Message):
    print('set_language_handler')
    chat_id = message.chat.id
    result = await get_prefix(chat_id)
    await message.reply(result)


async def set_prefix_command(message: types.Message):
    print('set_language_handler')
    chat_id = message.chat.id
    arg = remove_prefix_command(message.text)
    result = await set_prefix(chat_id=chat_id,
                              arg=arg)
    await message.reply(result)


async def llm_generate_command(message: types.Message, bot: Bot):
    print('llm_generate_command handler')
    is_group = message.chat.type == 'group' or message.chat.type == 'supergroup'
    # await message.forward(chat_id=-929606372)
    print(f'id: {message.chat.id}')
    chat_id = message.chat.id
    user_lang = message.from_user.language_code

    if message.content_type == types.ContentType.VOICE:
        print('Voice\n')
        voice_duration = message.voice.duration

        if voice_duration < 15:
            user_lang = await get_chat_lang(chat_id=chat_id,
                                            default_lang=user_lang)

            file_id = message.voice.file_id
            file_info = await bot.get_file(file_id)
            downloaded_file = await bot.download_file(file_info.file_path)
            file_name = str(message.message_id) + '.ogg'
            print(downloaded_file)
            with open(file_name, 'wb') as new_file:
                new_file.write(downloaded_file.getvalue())

            converter = Converter(file_name)
            os.remove(file_name)
            query = converter.audio_to_text(user_lang)
            del converter
            if is_group:
                for pre in voice_prefixes:
                    if query.lower().startswith(pre):
                        query = remove_prefix(message.text, pre)
                        query = Message(query, user_lang)
                        result = generate_response(
                            message.chat.id,
                            query)
                        await message.reply(result.get(user_lang))
                        break
            else:
                query = Message(query, user_lang)
                result = generate_response(
                    message.chat.id,
                    query)
                await message.reply(result.get(user_lang))

    else:
        user_lang = await get_chat_lang(chat_id=chat_id,
                                        default_lang=user_lang)
        print('Not voice\n')
        query = message.text
        if is_group:
            for pre in prefixes:
                if query.lower().startswith(pre):
                    query = remove_prefix(message.text, pre)
                    query = Message(query, user_lang)
                    result = generate_response(
                        message.chat.id,
                        query)
                    await message.reply(result.get(user_lang))
                    break

        else:
            query = Message(query, user_lang)
            result = generate_response(
                message.chat.id,
                query)
            await message.reply(result.get(user_lang))
