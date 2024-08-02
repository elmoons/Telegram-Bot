from aiogram import types, Router
from aiogram.filters import Command
from filters.is_private import IsChatPrivate
from filters.is_subscribed import IsSubscribed
from keyboards.make_keyboard import get_startup_inline_keyboard_markup, get_web_app_inline_keyboard_markup

router = Router()


@router.message(IsChatPrivate(), IsSubscribed())
async def command_start(message: types.Message):
    await message.answer(f"Откройте веб-приложения", reply_markup=get_web_app_inline_keyboard_markup())


@router.message(IsChatPrivate(), Command("start"))
async def command_start(message: types.Message):
    await message.answer(
        f"Для продолжения, вступите в группу и проверьте подписку",
        reply_markup=get_startup_inline_keyboard_markup())

