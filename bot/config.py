import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
    DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID", "")
    DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET", "")
    DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI", "http://localhost:5000/auth/callback")
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "change_this_secret_key")
    BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
    SERVER_ID = os.getenv("SERVER_ID", "")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "data/bot.db")

config = Config
