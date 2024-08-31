import sys
sys.path.append('..')
from data.get_config import get_config

config_file_name = "appsettings.json"
config = get_config(config_file_name)

BOT_TOKEN = config["bot_token"]
ADMIN_USER_ID = config["admin_user_id"]
GROUP_CHAT_ID = config["group_chat_id"]
GROUP_CHAT_URL = config["group_chat_url"]
WEB_APP_URL = config["web_app_url"]