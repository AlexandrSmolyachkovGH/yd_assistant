import asyncio
from aiogram import Bot, Dispatcher, types

from bot.config import bot_settings
from bot.routers import (
    auth,
    info,
    main_menu,
    reports,
    settings,
)

dp = Dispatcher()

dp.include_router(auth.router)
dp.include_router(main_menu.router)
dp.include_router(info.router)
dp.include_router(settings.router)
dp.include_router(reports.router)


async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="start", description="Запустить бота"),
        types.BotCommand(command="call_menu", description="Вызвать меню"),
        types.BotCommand(command="about", description="О боте"),
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    token = bot_settings.BOT_TOKEN.get_secret_value()
    bot = Bot(token)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
