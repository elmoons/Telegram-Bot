import sqlite3

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from backend.tgbot.data.config import GROUP_CHAT_URL
from backend.tgbot.filters import is_subscribed


def get_inline_keyboard_markup_for_subscription(language: str) -> InlineKeyboardMarkup:
    labels = {
        "ru": {"join_group": "Вступить в группу", "check_subscription": "Проверить подписку"},
        "en": {"join_group": "Join the group", "check_subscription": "Check subscription"}
    }

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=labels[language]["join_group"], url=GROUP_CHAT_URL))
    builder.row(InlineKeyboardButton(text=labels[language]["check_subscription"], callback_data="check_subscription"))
    return builder.as_markup()


async def get_menu_inline_keyboard_markup(user_id: int, language: str) -> InlineKeyboardMarkup:
    labels = {
        "ru": {"start": "Старт", "сhange_language": "Сменить язык", "go_to_channel": "Перейти в канал", "tech_support": "Тех поддержка"},
        "en": {"start": "Start", "сhange_language": "Change language", "go_to_channel": "Go to channel", "tech_support": "Tech support"},
    }

    is_user_subscribed = await is_subscribed.check(user_id)
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT deposit FROM UsersPostback WHERE telegram_id = ?", (user_id,))
    user = cursor.fetchone()
    has_deposit = user and float(user[0]) > 0

    builder = InlineKeyboardBuilder()

    if not is_user_subscribed:
        start_callback_data = "subscribe_to_group"
    elif not has_deposit:
        start_callback_data = "registration_replenishment"
    else:
        start_callback_data = "open_web_app"  # Обработка через callback

    builder.row(InlineKeyboardButton(text=labels[language]["start"], callback_data=start_callback_data))
    builder.row(InlineKeyboardButton(text=labels[language]["go_to_channel"], url=GROUP_CHAT_URL))
    builder.row(
        InlineKeyboardButton(text=labels[language]["сhange_language"], callback_data="сhange_language"),
        InlineKeyboardButton(text=labels[language]["tech_support"], url="https://t.me/stas_astapov")
    )

    return builder.as_markup()



def get_languages_inline_keyboard_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Русский", callback_data="ru"))
    builder.row(InlineKeyboardButton(text="English", callback_data="en"))
    return builder.as_markup()
