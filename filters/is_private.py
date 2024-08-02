from aiogram import types
from aiogram.filters import Filter


class IsChatPrivate(Filter):
    async def __call__(self, message: types.Message):
        return message.chat.type == "private"
