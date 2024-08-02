from aiogram import Bot, Dispatcher

from backend.tgbot.data import config

bot = Bot(config.BOT_TOKEN)

dispatcher = Dispatcher()
