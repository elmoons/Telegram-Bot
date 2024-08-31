import json
import os
import sys
import keyboard


def get_config(path):
    if not os.path.exists(path):
        with open(path, 'w') as config_path:
            config = {
                "bot_token": "BOT_TOKEN",
                "admin_user_id": "ADMIN_USER_ID",
                "group_chat_id": "@group_chat_id",
                "group_chat_url": "https://t.me/group_chat_url",
                "web_app_url": "https://web_app_url"
            }
            json.dump(config, config_path)
            print(f"Не нашел файл {path}, в следствии чего он был создан, "
                  f"поменяйте в нем данные и перезапустите приложение")
        keyboard.read_key()
        sys.exit()

    with open(path) as path:
        return json.load(path)