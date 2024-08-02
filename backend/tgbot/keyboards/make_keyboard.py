from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from backend.tgbot.data.config import GROUP_CHAT_URL, WEB_APP_URL


def get_startup_inline_keyboard_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Вступить в группу", url=GROUP_CHAT_URL))
    builder.row(InlineKeyboardButton(text="Проверить подписку", callback_data="Проверить подписку"))
    return builder.as_markup()


def get_web_app_inline_keyboard_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Перейти", web_app=WebAppInfo(url=WEB_APP_URL)))
    return builder.as_markup()
