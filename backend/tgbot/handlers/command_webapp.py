from aiogram import types, Router, F
from aiogram.filters import Command

from backend.tgbot.filters import is_subscribed
from backend.tgbot.keyboards import make_keyboard
from backend.tgbot.loader import user_repository

router = Router()

text1 = {
    "ru": "Откройте веб-приложение",
    "en": "Open the web application"
}

text2 = {
    "ru": "Для продолжения, вступите в группу и проверьте подписку",
    "en": "To continue, please join the group and check your subscription."
}


# @router.callback_query(F.data == "check_subscription")
# async def handle_check_subscription(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     language = await user_repository.get_language_or_none(user_id)
#     if language is None:
#         language = callback_query.from_user.language_code
#     if await is_subscribed.check(user_id):
#         await callback_query.message.edit_text(
#             text1.get(language, text1["en"]),
#             reply_markup=make_keyboard.get_web_app_inline_keyboard_markup(language))
#     else:
#         await callback_query.message.delete()
#         await callback_query.message.answer(
#             text2[language],
#             reply_markup=make_keyboard.get_inline_keyboard_markup_for_subscription(language))
#
#
# @router.message(Command("webapp"))
# async def handle_when_subscribed(message: types.Message):
#     user_id = message.from_user.id
#     language = await user_repository.get_language_or_none(user_id)
#
#     if language is None:
#         language = message.from_user.language_code
#
#     if await is_subscribed.check(user_id):
#         language = message.from_user.language_code
#         await message.answer(
#             text1.get(language, text1["en"]),
#             reply_markup=make_keyboard.get_web_app_inline_keyboard_markup(language))
#     else:
#         await message.answer(
#             text2[language],
#             reply_markup=make_keyboard.get_inline_keyboard_markup_for_subscription(language))