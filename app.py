import asyncio
import threading

from bot.bot import bot, start_bot
from web.app import app


def run_web_app():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web_app, daemon=True)
    web_thread.start()
    asyncio.run(start_bot())
