import sqlite3
import sys
sys.path.append('..')
from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, WebAppInfo, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import asyncio
from filters import is_subscribed
from filters.is_private import IsChatPrivate
from keyboards import make_keyboard
from aiogram.fsm.context import FSMContext
from data.config import WEB_APP_URL, BOT_TOKEN, GROUP_CHAT_ID
from loader import user_repository

router = Router()

state_language = "language"

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()


async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=GROUP_CHAT_ID, user_id=user_id)
        return member.status not in ("left", "kicked")
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
        return False


@router.callback_query(F.data == "open_web_app")
async def process_check_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    language = await user_repository.get_language_or_none(user_id)
    if language is None:
        language = callback_query.from_user.language_code

    if is_subscribed:
        texts = {
            "ru": {
                "subscription_confirmed": "Подписка подтверждена. Открываем мини-приложение...",
                "open_web_app": "Нажмите кнопку, чтобы открыть мини-приложение:"
            },
            "en": {
                "subscription_confirmed": "Subscription confirmed. Opening the mini-app...",
                "open_web_app": "Click the button to open the mini-app:"
            }
        }

        await callback_query.answer(texts[language]["subscription_confirmed"])
        webapp_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Открыть мини-приложение", web_app=WebAppInfo(url=WEB_APP_URL))]
            ]
        )
        message = await bot.send_message(user_id, texts[language]["open_web_app"], reply_markup=webapp_keyboard)

        await asyncio.sleep(15)
        await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    else:
        texts = {
            "ru": {
                "not_subscribed": "Вы не подписаны на наш канал.",
                "please_subscribe": "Пожалуйста, подпишитесь на наш канал, чтобы получить доступ к мини-приложению.",
                "subscribe_button": "Подписаться на канал",
                "check_subscription": "Проверить подписку"
            },
            "en": {
                "not_subscribed": "You are not subscribed to our channel.",
                "please_subscribe": "Please subscribe to our channel to access the mini-app.",
                "subscribe_button": "Subscribe to channel",
                "check_subscription": "Check subscription"
            }
        }

        channel_info = await bot.get_chat(GROUP_CHAT_ID)
        channel_username = channel_info.username or f"https://t.me/c/{str(GROUP_CHAT_ID)[4:]}"
        await callback_query.answer(texts[language]["not_subscribed"], show_alert=True)
        subscribe_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=texts[language]["subscribe_button"],
                                      url=f"https://t.me/{channel_username}")],
                [InlineKeyboardButton(text=texts[language]["check_subscription"], callback_data="check_subscription")]
            ]
        )
        await bot.send_message(user_id, texts[language]["please_subscribe"], reply_markup=subscribe_keyboard)


@router.callback_query(F.data == "registration_replenishment")
async def logic_of_reg(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Проверяем, подписан ли пользователь на группу
    if not await is_subscribed.check(user_id):
        language = await user_repository.get_language_or_none(user_id)
        if language is None:
            language = callback_query.from_user.language_code

        text = {
            "ru": "Для продолжения, нажми - 💸💸ВСТУПИТЬ В ГРУППУ💸💸",
            "en": "To continue, click - 💸💸JOIN THE GROUP💸💸"
        }

        await callback_query.message.answer(
            text.get(language, text["en"]),
            reply_markup=make_keyboard.get_inline_keyboard_markup_for_subscription(language)
        )
        return

    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()

    # Получаем язык пользователя
    language = await user_repository.get_language_or_none(user_id)
    if language is None:
        language = callback_query.from_user.language_code

    # Проверяем, внесен ли депозит
    cursor.execute("SELECT deposit FROM UsersPostback WHERE telegram_id = ?", (user_id,))
    user = cursor.fetchone()

    if user and float(user[0]) > 0:
        # Если депозит внесен, запускаем приложение
        await start_app_if_deposited(callback_query, language)
    else:
        referral_link = f"https://1wfdnu.life/casino/list?open=register&p=j9ks&sub1={user_id}"

        # Тексты на разных языках
        text = {
            "ru": """👋<b>Здравствуйте!</b>

Чтобы получить максимальную эффективность от использования данного бота, необходимо выполнить следующие шаги: 

1. Зарегистрируйте новый аккаунт - если у Вас уже есть аккаунт, пожалуйста, покиньте его и зарегистрируйте новый. 
2. Используйте промокод <b>VR97</b> при регистрации нового аккаунта. Это важно, так как наш <b>ИИ</b> работает только с новыми аккаунтами. 
3. После регистрации нажмите на кнопку <b>“Проверить регистрацию”</b>. 
4. Если Вы не выполните эти шаги, наш бот не сможет добавить Ваш аккаунт в свою базу данных, и предоставляемые им сигналы могут не подойти. 

Спасибо за понимание!""",
            "en": """👋<b>Hello!</b>

To apply the effectiveness of using this bot, you need to adjust the following steps: 

1. Register a new account - if you already have an account, please leave it and register a new account. 
2. Use the <b>VR97</b> promotional code when registering a new account. This is important, since our <b>AI</b> only works with new accounts. 
3. After registration, click on the <b>"Check Registration"</b> button. 
4. If you do not complete these steps, our bot will not be able to add your account to its data resources, and the signals it provides may not be captured. 

Thank you for your understanding!"""
        }

        # Создание кнопок
        builder = InlineKeyboardBuilder()
        builder.button(text="📲РЕГИСТРАЦИЯ" if language == "ru" else "📲REGISTER", url=referral_link)
        builder.button(text="🔍ПРОВЕРИТЬ РЕГИСТРАЦИЮ" if language == "ru" else "🔍CHECK REGISTRATION",
                       callback_data="check_registration")
        builder.adjust(1, 1)

        await callback_query.message.answer(text[language], reply_markup=builder.as_markup(), parse_mode='HTML')


async def start_app_if_deposited(callback_query: types.CallbackQuery, language: str):
    user_id = callback_query.from_user.id

    # Проверяем, подписан ли пользователь на группу
    if not await is_subscribed.check(user_id):
        text = {
            "ru": "Для продолжения, нажми 💸💸ВСТУПИТЬ В ГРУППУ💸💸",
            "en": "To continue, click - 💸💸JOIN THE GROUP💸💸"
        }

        await callback_query.message.answer(
            text.get(language, text["en"]),
            reply_markup=make_keyboard.get_inline_keyboard_markup_for_subscription(language)
        )
        return

    text = {
        "ru_start_app": "Теперь вы можете запустить приложение, нажав на кнопку Получить сигнал в главном меню!",
        "en_start_app": "Now you can start the application by clicking on the Get a signal button in the main menu!"
    }

    # Отправляем сообщение о запуске приложения
    await callback_query.message.answer(text[f"{language}_start_app"])

    # Отправляем главное меню
    await handle_check_subscription(callback_query)


@router.callback_query(F.data == "check_registration")
async def callback_query(call: CallbackQuery):
    user_id = call.from_user.id
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()

    # Получаем язык пользователя
    language = await user_repository.get_language_or_none(user_id)
    if language is None:
        language = call.from_user.language_code

    # Тексты на разных языках
    text = {
        "ru_registered": "Вы зарегистрированы. Выберите действие:",
        "en_registered": "You are registered. Please select an action:",
        "ru_not_registered": "Вы не зарегистрированы.",
        "en_not_registered": "You are not registered."
    }

    if call.data == "check_registration":
        cursor.execute("SELECT * FROM UsersPostback WHERE telegram_id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            referral_link = f"https://1wfdnu.life/casino/list?open=register&p=j9ks&sub1={user_id}"

            # Проверяем, внесен ли депозит
            cursor.execute("SELECT deposit FROM UsersPostback WHERE telegram_id = ?", (user_id,))
            deposit_info = cursor.fetchone()

            if deposit_info and float(deposit_info[0]) > 0:
                await start_app_if_deposited(call, language)
            else:
                builder = InlineKeyboardBuilder()
                builder.button(text="💰ПОПОЛНИТЬ БАЛАНС" if language == "ru" else "🔍TOP-UP", url=referral_link)
                builder.button(text="🔍ПРОВЕРИТЬ ПОПОЛНЕНИЕ" if language == "ru" else "🔍CHECK REPLACEMENT",
                               callback_data="check_deposit")
                builder.adjust(1, 1)

                await call.message.answer(text[f"{language}_registered"], reply_markup=builder.as_markup())

        else:
            await call.answer(text[f"{language}_not_registered"], show_alert=True)


@router.callback_query(F.data == "check_deposit")
async def callback_query(call: CallbackQuery):
    user_id = call.from_user.id
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()

    # Получаем язык пользователя
    language = await user_repository.get_language_or_none(user_id)
    if language is None:
        language = call.from_user.language_code

    # Тексты на разных языках
    text = {
        "ru_no_deposit": "Депозит не найден.",
        "en_no_deposit": "Deposit not found.",
        "ru_start_app": "Теперь вы можете запустить приложение, нажав на кнопку Получить сигнал в главном меню!",
        "en_start_app": "Now you can start the application by clicking on the Get a signal button in the main menu!"
    }

    if call.data == "check_deposit":
        cursor.execute("SELECT deposit FROM UsersPostback WHERE telegram_id = ?", (user_id,))
        user = cursor.fetchone()

        if user and float(user[0]) > 0:
            # Успешное пополнение

            # Показываем главное меню сразу после пополнения депозита
            await handle_check_subscription(call)
        else:
            await call.answer(text[f"{language}_no_deposit"], show_alert=True)


@router.callback_query(F.data == "сhange_language")
async def set_language(callback_query: types.CallbackQuery, state: FSMContext):
    text = {
        "ru": "Выберите язык:",
        "en": "Select language:"
    }

    language = await user_repository.get_language_or_none(callback_query.message.from_user.id)
    if language is None:
        language = callback_query.message.from_user.language_code

    await callback_query.message.edit_text(
        text.get(language, text["en"]),
        reply_markup=make_keyboard.get_languages_inline_keyboard_markup())
    await state.set_state(state_language)


@router.callback_query(F.data == "check_subscription")
async def handle_check_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    language = await user_repository.get_language_or_none(user_id)
    if language is None:
        language = callback_query.from_user.language_code
    if await is_subscribed.check(user_id):
        text = {
            "ru": "🏡Главное меню",
            "en": "🏡Main menu"
        }

        await callback_query.message.edit_text(
            text.get(language, text["en"]),
            reply_markup=await make_keyboard.get_menu_inline_keyboard_markup(user_id, language))
    else:
        text = {
            "ru": "Для продолжения, нажми - 💸💸ВСТУПИТЬ В ГРУППУ💸💸",
            "en": "To continue, click - 💸💸JOIN THE GROUP💸💸"
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

    # Определяем URL изображения в зависимости от языка
    await message.answer(
        text.get(language, text["en"]),
        reply_markup=make_keyboard.get_languages_inline_keyboard_markup()
    )
    await state.set_state(state_language)


@router.callback_query(StateFilter(state_language))
async def set_language(callback_query: types.CallbackQuery, state: FSMContext):
    print(callback_query)
    language = callback_query.data

    await user_repository.set_or_update_language(callback_query.from_user.id, language)

    text = {
        "ru": "Выбранный язык успешно сохранен!",
        "en": "The selected language has been successfully saved!"
    }

    await callback_query.message.edit_text(text[language])
    await state.clear()
    await handle_check_subscription(callback_query)