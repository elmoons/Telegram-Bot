import sqlite3

from backend.tgbot.db.app_database import AppDatabase


class UserRepository:
    def __init__(self, app_database: AppDatabase):
        self.app_dataBase: AppDatabase = app_database

    async def set_or_update_language(self, user_id: int, language: str):
        connection = sqlite3.connect(self.app_dataBase.path)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,))
        result = cursor.fetchall()
        if len(result) == 0:
            cursor.execute('INSERT INTO Users (user_id, language) VALUES (?, ?)',
                           (user_id, language)
                           )
        else:
            cursor.execute('UPDATE Users SET language = ? WHERE user_id = ?', (language, user_id))
        connection.commit()
        connection.close()

    async def get_language_or_none(self, user_id: int):
        connection = sqlite3.connect(self.app_dataBase.path)
        cursor = connection.cursor()
        cursor.execute('SELECT language FROM Users WHERE user_id = ?', (user_id,))
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        if len(result) == 0:
            return None
        return result[0][0]