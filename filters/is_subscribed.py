from aiogram import types
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Filter

from data.config import GROUP_CHAT_ID
from loader import bot


class IsSubscribed(Filter):
    async def __call__(self, message: types.Message):
        chat_member = await bot.get_chat_member(
            chat_id=GROUP_CHAT_ID,
            user_id=message.from_user.id
        )
        if (chat_member.status == ChatMemberStatus.LEFT or
                chat_member.status == ChatMemberStatus.KICKED):
            return False
        return True
