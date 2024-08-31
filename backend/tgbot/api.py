from fastapi import FastAPI, Depends, Query
import sqlite3
import requests
from data.config import BOT_TOKEN, ADMIN_USER_ID

app = FastAPI()

# Инициализация базы данных и создание таблицы при старте приложения
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS UsersPostback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id TEXT UNIQUE,
                site_login TEXT,
                deposit REAL DEFAULT 0
            )
        ''')
        conn.commit()

init_db()

# Зависимость для получения курсора базы данных
def get_db():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    try:
        yield conn.cursor()
        conn.commit()
    finally:
        conn.close()

def send_notification(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': ADMIN_USER_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    print(f"URL: {url}")  # Для отладки
    print(f"Payload: {payload}")  # Проверка отправляемых данных
    print(f"Telegram Response: {response.json()}")  # Логирование ответа Telegram

# Обработчик GET-запроса для /postback/
@app.get("/postback/")
async def postback(user_id: str = Query(...), sub1: str = Query(...), amount: float = Query(None), cursor=Depends(get_db)):
    telegram_id = sub1
    deposit_amount = amount
    try:
        print(f"Received query parameters - User ID: {user_id}, Telegram ID: {telegram_id}, Deposit Amount: {deposit_amount}")

        cursor.execute("SELECT deposit FROM UsersPostback WHERE telegram_id = ?", (telegram_id,))
        user = cursor.fetchone()

        if user:
            current_deposit = user[0]
            if deposit_amount is not None:
                if current_deposit == 0:
                    cursor.execute("""
                        UPDATE UsersPostback
                        SET deposit = ?
                        WHERE telegram_id = ?
                    """, (deposit_amount, telegram_id))
                    send_notification(
                        f"Пользователь с Telegram ID {telegram_id} внес первый депозит {deposit_amount}. Логин 1WIN: {user_id}")
                    return {"status": "success", "message": "Deposit recorded successfully"}
                else:
                    return {"status": "error", "message": "Deposit already recorded"}
            else:
                return {"status": "error", "message": "User is already registered"}
        else:
            deposit_value = deposit_amount if deposit_amount is not None else 0.0
            cursor.execute("""
                INSERT INTO UsersPostback (telegram_id, site_login, deposit)
                VALUES (?, ?, ?)
            """, (telegram_id, user_id, deposit_value))
            if deposit_amount is not None:
                send_notification(
                    f"Пользователь с Telegram ID {telegram_id} зарегистрировался и внес депозит {deposit_amount}. Логин 1WIN: {user_id}")
            else:
                send_notification(
                    f"Пользователь с Telegram ID: {telegram_id} зарегистрировался. Логин 1WIN: {user_id}")
            return {"status": "success", "message": "User registered successfully"}

    except ValueError:
        return {"status": "error", "message": "Invalid data format"}

    return {"status": "error", "message": "No data provided"}