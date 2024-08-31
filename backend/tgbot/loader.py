from aiogram import Bot, Dispatcher

from data import config
from db.app_database import AppDatabase
from db.user_repository import UserRepository

bot = Bot(config.BOT_TOKEN)

dispatcher = Dispatcher()

app_database = AppDatabase()
user_repository = UserRepository(app_database)