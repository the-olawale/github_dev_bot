import os
from dotenv import load_dotenv

load_dotenv()

telegramBotToken = os.getenv("TELEGRAM_BOT_TOKEN")
gitHubToken = os.getenv("GITHUB_TOKEN")