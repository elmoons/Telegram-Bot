import sqlite3


class AppDatabase:
    path: str = "database.db"

    def up(self):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS Users(
                    user_id INTEGER,
                    language TEXT)''')
        connection.commit()
        connection.close()