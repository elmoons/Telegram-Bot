from aiogram import Bot, Dispatcher

from backend.tgbot.data import config
from backend.tgbot.db.app_database import AppDatabase
from backend.tgbot.db.user_repository import UserRepository

bot = Bot(config.BOT_TOKEN)

dispatcher = Dispatcher()

app_database = AppDatabase()
user_repository = UserRepository(app_database)
