from aiogram import types
from aiogram.dispatcher.filters import BaseFilter


class StartWithFilter(BaseFilter):
    commands: list[str]

    async def __call__(self, message: types.Message):
        if message.text is not None:
            for command in self.commands:
                if message.text.startswith(command):
                    return True
        return False
