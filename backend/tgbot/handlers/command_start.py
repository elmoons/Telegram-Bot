from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter

from backend.tgbot.filters import is_subscribed
from backend.tgbot.filters.is_private import IsChatPrivate
from backend.tgbot.keyboards import make_keyboard
from aiogram.fsm.context import FSMContext

from backend.tgbot.loader import user_repository

router = Router()

state_language = "language"


@router.callback_query(F.data == "check_subscription")
async def handle_check_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    language = await user_repository.get_language_or_none(user_id)
    if language is None:
        language = callback_query.from_user.language_code
    if await is_subscribed.check(user_id):
        text = {
            "ru": "Откройте веб-приложение",
            "en": "Open the web application"
        }

        await callback_query.message.edit_text(
            text.get(language, text["en"]),
            reply_markup=make_keyboard.get_web_app_inline_keyboard_markup(language))
    else:
        text = {
            "ru": "Для продолжения, вступите в группу и проверьте подписку",
            "en": "To continue, please join the group and check your subscription."
        }

        await callback_query.message.delete()
        await callback_query.message.answer(
            text.get(language, text["en"]),
            reply_markup=make_keyboard.get_inline_keyboard_markup_for_subscription(language))


@router.message(IsChatPrivate(), Command("start"))
async def command_start(message: types.Message, state: FSMContext):
    await state.clear()
    text = {
        "ru": "Добро пожаловать! Пожалуйста, выберите язык:",
        "en": "Welcome! Please select your language:"
    }

    language = await user_repository.get_language_or_none(message.from_user.id)
    if language is None:
        language = message.from_user.language_code

    await message.answer(
        text.get(language, text["en"]),
        reply_markup=make_keyboard.get_languages_inline_keyboard_markup())
    await state.set_state(state_language)


@router.callback_query(StateFilter(state_language))
async def set_language(callback_query: types.CallbackQuery, state: FSMContext):
    language = callback_query.data

    await user_repository.set_or_update_language(callback_query.from_user.id, language)

    text = {
        "ru": "Выбранный язык успешно сохранен!",
        "en": "The selected language has been successfully saved!"
    }

    await callback_query.message.edit_text(text[language])
    await state.clear()
    await handle_check_subscription(callback_query)
