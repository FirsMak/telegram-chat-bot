from aiogram import Bot
from aiogram import Dispatcher
import asyncio
from configuration import TELEGRAM_TOKEN
from commands import register_commands
# Opening JSON filef = open('data.json')
# storage = RedisStorage2(
#    host=config.REDIS_HOST,
#    port=config.REDIS_PORT,
#    db=config.REDIS_DB,
#    password=config.REDIS_PASSWORD,
# )


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()

    # dp.middleware.setup(ThrottlingMiddleware())
    register_commands(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
