from aiogram import types, Router, F
from aiogram.filters import Command
from backend.tgbot.filters.is_private import IsChatPrivate
from backend.tgbot.filters.is_subscribed import IsSubscribed
from backend.tgbot.keyboards.make_keyboard import get_startup_inline_keyboard_markup, get_web_app_inline_keyboard_markup

router = Router()


@router.message(IsChatPrivate(), IsSubscribed())
async def send_web_app_link(message: types.Message):
    await message.answer(f"Откройте веб-приложения", reply_markup=get_web_app_inline_keyboard_markup())


@router.callback_query(F.data == "Проверить подписку")
async def handle_data_subscribed(callback_query: types.CallbackQuery):
    if(await IsSubscribed().check(callback_query.from_user.id)):
        await send_web_app_link(callback_query.message)
    else:
        await callback_query.message.delete()
        await command_start(callback_query.message)


@router.message(IsChatPrivate(), Command("start"))
async def command_start(message: types.Message):
    await message.answer(
        f"Для продолжения, вступите в группу и проверьте подписку",
        reply_markup=get_startup_inline_keyboard_markup())
