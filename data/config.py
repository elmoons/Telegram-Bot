from data.get_config import get_config

config_file_name = "config.json"
config = get_config(config_file_name)

BOT_TOKEN = config["bot_token"]
GROUP_CHAT_ID = config["group_chat_id"]
GROUP_CHAT_URL = config["group_chat_url"]
WEB_APP_URL = config["web_app_url"]