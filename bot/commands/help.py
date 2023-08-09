from data import get_all_commands
from aiogram import types


async def help_command(message: types.Message):
    print('help_handler')
    result = await get_all_commands()
    await message.reply(result)
