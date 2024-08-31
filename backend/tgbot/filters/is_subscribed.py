import sys
from typing import Union
sys.path.append('..')
from aiogram import types
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Filter

from data.config import GROUP_CHAT_ID
from loader import bot

async def check(user_id) -> bool:
    chat_member = await bot.get_chat_member(
        chat_id=GROUP_CHAT_ID,
        user_id=user_id
    )
    if (chat_member.status == ChatMemberStatus.LEFT or
            chat_member.status == ChatMemberStatus.KICKED):
        return False
    return True


class IsSubscribedOnMessage(Filter):
    async def __call__(self, message: types.Message):
        return await check(message.from_user.id)


class IsSubscribedOnCallbackQuery(Filter):
    async def __call__(self, callback_query: types.CallbackQuery):
        return await check(callback_query.from_user.id)