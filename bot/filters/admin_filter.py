from aiogram import types, Bot
from aiogram.dispatcher.filters import BaseFilter, Command


class AdminCommandsFilter(Command):
    admins = ['administrator', 'creator']

    async def __call__(self, message: types.Message, bot: Bot):
        isCommand = await super().__call__(message, bot)
        print(f'is ccommand - {isCommand}')
        if isCommand:
            member = await bot.get_chat_member(message.chat.id,
                                               message.from_user.id)
            print(member.status)
            if member.status in self.admins:
                return True

        return False
