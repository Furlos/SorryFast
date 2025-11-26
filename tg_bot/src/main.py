import asyncio

from aiogram import Bot, Dispatcher
from config import token
from handlers.start import start_router
from handlers.profiles.router import profile_router


async def main():
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(profile_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())