import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
import sqlite3
import requests

app = FastAPI()
load_dotenv()

# Получаем переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")


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


# Обработчик POST-запроса для /postback/
@app.post("/postback/")
async def postback(request: Request, cursor=Depends(get_db)):
    data = await request.json()
    raw_data = data.get('data')

    if raw_data:
        print(f"Received data: {data}")
        try:
            parts = raw_data.split()
            if len(parts) == 3:
                user_id, telegram_id, deposit_amount = parts
                deposit_amount = float(deposit_amount)
            elif len(parts) == 2:
                user_id, telegram_id = parts
                deposit_amount = None
            else:
                return {"status": "error", "message": "Invalid data format"}

            print(f"Parsed values - User ID: {user_id}, Telegram ID: {telegram_id}, Deposit Amount: {deposit_amount}")

            cursor.execute("SELECT deposit FROM UsersPostback WHERE telegram_id = ?", (telegram_id,))
            user = cursor.fetchone()

            if user:
                current_deposit = user[0]
                if deposit_amount is not None and current_deposit == 0:
                    cursor.execute("""
                        UPDATE UsersPostback
                        SET deposit = ?
                        WHERE telegram_id = ?
                    """, (deposit_amount, telegram_id))
                    send_notification(
                        f"Пользователь с Telegram ID {telegram_id} внес первый депозит {deposit_amount}. Логин 1WIN: {user_id}")
                    return {"status": "success", "message": "Deposit recorded successfully"}
                elif deposit_amount is None:
                    return {"status": "error", "message": "User is already registered"}
                else:
                    return {"status": "error", "message": "Deposit already recorded"}
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

#
# # Запуск приложения
# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host="0.0.0.0", port=8000)
import sqlite3


def view_users_postback():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM UsersPostback")

        # Получаем все строки результата
        rows = cursor.fetchall()

        # Проверяем, есть ли записи и выводим их
        if not rows:
            print("Таблица UsersPostback пуста.")
        else:
            for row in rows:
                print(row)



view_users_postback()
def clear_users_postback():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM UsersPostback")
        conn.commit()
clear_users_postback()  # Очистка таблицы перед добавлением новых данных
