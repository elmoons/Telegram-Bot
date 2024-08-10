from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from backend.tgbot.data.config import GROUP_CHAT_URL, WEB_APP_URL


def get_inline_keyboard_markup_for_subscription(language: str) -> InlineKeyboardMarkup:
    labels = {
        "ru": {"join_group": "Вступить в группу", "check_subscription": "Проверить подписку"},
        "en": {"join_group": "Join the group", "check_subscription": "Check subscription"}
    }

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=labels[language]["join_group"], url=GROUP_CHAT_URL))
    builder.row(InlineKeyboardButton(text=labels[language]["check_subscription"], callback_data="check_subscription"))
    return builder.as_markup()


def get_menu_inline_keyboard_markup(language: str) -> InlineKeyboardMarkup:
    labels = {
        "ru": {"start": "Старт", "сhange_language": "Сменить язык", "go_to_channel": "Перейти в канал"},
        "en": {"start": "Start", "сhange_language": "Change language", "go_to_channel": "Go to channel"},
    }

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=labels[language]["start"], web_app=WebAppInfo(url=WEB_APP_URL)))
    builder.row(InlineKeyboardButton(text=labels[language]["сhange_language"], callback_data="сhange_language"))
    builder.row(InlineKeyboardButton(text=labels[language]["go_to_channel"], url=GROUP_CHAT_URL))
    return builder.as_markup()


def get_languages_inline_keyboard_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Русский", callback_data="ru"))
    builder.row(InlineKeyboardButton(text="English", callback_data="en"))
    return builder.as_markup()
