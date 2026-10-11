from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# .env を読み込む
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

class Config:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
    DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID", "")
    DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET", "")
    DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI", "http://localhost:5000/auth/callback")
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "change_this_secret_key")
    BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
    SERVER_ID = os.getenv("SERVER_ID", "")
    DATABASE_PATH = os.getenv("DATABASE_PATH", str(DATA_DIR / "bot.db"))

    @classmethod
    def validate(cls) -> None:
        required = [
            "DISCORD_TOKEN",
            "DISCORD_CLIENT_ID",
            "DISCORD_CLIENT_SECRET",
        ]
        missing = [key for key in required if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Missing required env vars: {', '.join(missing)}")

config = Config
