from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from backend.tgbot.filters.is_private import IsChatPrivate
from backend.tgbot.filters.is_subscribed import IsSubscribed
from backend.tgbot.keyboards import make_keyboard
from aiogram.fsm.context import FSMContext

router = Router()

state_language = "language"


@router.message(IsChatPrivate(), Command("start"))
async def command_start(message: types.Message, state: FSMContext):
    await message.answer(
        "Welcome! Please select your language:",
        reply_markup=make_keyboard.get_languages_inline_keyboard_markup())
    await state.set_state(state_language)


@router.callback_query(StateFilter(state_language))
async def set_language_and_prompt_subscription(callback_query: types.CallbackQuery, state: FSMContext):
    selected_language = callback_query.data
    await state.update_data(language=selected_language)
    await handle_data_subscribed(callback_query, state)


@router.message(IsChatPrivate(), IsSubscribed())
async def send_web_app(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", "ru")

    text = {
        "ru": "Откройте веб-приложение",
        "en": "Open the web application"
    }

    await message.edit_text(
        text[language],
        reply_markup=make_keyboard.get_web_app_inline_keyboard_markup(language))


@router.callback_query(StateFilter(None), F.data == "check_subscription")
async def handle_data_subscribed(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    language = data.get("language", "ru")

    if await IsSubscribed().check(callback_query.from_user.id):
        await send_web_app(callback_query.message, state)
    else:
        text = {
            "ru": "Для продолжения, вступите в группу и проверьте подписку",
            "en": "To continue, please join the group and check your subscription."
        }
        await callback_query.message.delete()
        await callback_query.message.answer(
            text[language],
            reply_markup=make_keyboard.get_startup_inline_keyboard_markup(language))
    await state.set_state(None)
