import asyncio
from aiogram.types import BotCommand
from backend.tgbot.handlers import command_start
from loader import dispatcher, bot, app_database


async def set_default_commands():
    await bot.set_my_commands([
        BotCommand(command="start", description="start bot"),
    ])


def include_routers():
    routers = [command_start.router]
    for router in routers:
        dispatcher.include_router(router)


async def main():
    app_database.up()
    include_routers()
    await set_default_commands()
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
