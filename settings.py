import os
from dotenv import load_dotenv

# Load the environmet variables from the .env file
load_dotenv()

bot_access_password = os.getenv("BOT_ACCESS_PASSWORD")
telegram_api_token = os.getenv("TELEGRAM_API_TOKEN")
storage_location = os.getenv("STORAGE_LOCATION", "local")
db_logging = bool(int(os.getenv("DBLOGGING", 0)))
dropbox_api_token = os.getenv("DROPBOX_API_TOKEN")

