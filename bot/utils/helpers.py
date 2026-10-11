from __future__ import annotations

import os

from bot.config import config


def ensure_required_env() -> None:
    config.validate()


def get_prefix() -> str:
    return config.BOT_PREFIX


def get_database_path() -> str:
    return config.DATABASE_PATH
