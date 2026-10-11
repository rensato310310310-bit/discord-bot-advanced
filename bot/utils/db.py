import sqlite3
from pathlib import Path

from bot.config import config

DB_PATH = Path(config.DATABASE_PATH)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_number INTEGER NOT NULL UNIQUE,
                user_id TEXT NOT NULL,
                guild_id TEXT NOT NULL,
                channel_id TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS role_panels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT NOT NULL,
                channel_id TEXT NOT NULL,
                message_id TEXT NOT NULL,
                role_name TEXT NOT NULL,
                role_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS pinned_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id TEXT NOT NULL,
                channel_id TEXT NOT NULL,
                message_id TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS auth_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discord_user_id TEXT NOT NULL UNIQUE,
                email TEXT,
                access_token TEXT,
                refresh_token TEXT,
                expires_at TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()
    finally:
        conn.close()


def get_next_ticket_number() -> int:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT COALESCE(MAX(ticket_number), 0) + 1 AS next_number FROM tickets"
        ).fetchone()
        return int(row["next_number"])
    finally:
        conn.close()


def save_auth_user(discord_user_id: str, email: str | None, access_token: str | None, refresh_token: str | None, expires_at: str | None) -> None:
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO auth_users (discord_user_id, email, access_token, refresh_token, expires_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(discord_user_id)
            DO UPDATE SET
                email = excluded.email,
                access_token = excluded.access_token,
                refresh_token = excluded.refresh_token,
                expires_at = excluded.expires_at
            """,
            (discord_user_id, email, access_token, refresh_token, expires_at),
        )
        conn.commit()
    finally:
        conn.close()


def save_role_panel(guild_id: str, channel_id: str, message_id: str, role_name: str, role_id: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO role_panels(guild_id, channel_id, message_id, role_name, role_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (guild_id, channel_id, message_id, role_name, role_id),
        )
        conn.commit()
    finally:
        conn.close()


def save_pinned_message(guild_id: str, channel_id: str, message_id: str, content: str) -> None:
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO pinned_messages(guild_id, channel_id, message_id, content)
            VALUES (?, ?, ?, ?)
            """,
            (guild_id, channel_id, message_id, content),
        )
        conn.commit()
    finally:
        conn.close()
