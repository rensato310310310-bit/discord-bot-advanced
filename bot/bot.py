import asyncio
import threading

import discord
from discord.ext import commands

from bot.config import config
from bot.utils.db import init_db

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config.BOT_PREFIX, intents=intents)

@bot.event
async def on_ready():
    init_db()
    print(f"Bot logged in as {bot.user} (ID: {bot.user.id})")

@bot.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send("pong!")

async def start_bot():
    await bot.load_extension("bot.cogs.ticket_cog")
    await bot.load_extension("bot.cogs.role_panel_cog")
    await bot.load_extension("bot.cogs.pinned_message_cog")
    await bot.start(config.DISCORD_TOKEN)
