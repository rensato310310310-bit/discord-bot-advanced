import discord
from discord.ext import commands

from bot.services.pinned_message_service import send_pinned_message, update_pinned_message
from bot.utils.db import save_pinned_message


class PinnedMessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pinmsg")
    async def pinmsg(self, ctx: commands.Context, *, content: str):
        message = await update_pinned_message(ctx.channel, content)
        save_pinned_message(
            guild_id=str(ctx.guild.id),
            channel_id=str(ctx.channel.id),
            message_id=str(message.id),
            content=content,
        )
        await ctx.send(f"固定メッセージを更新しました: {message.jump_url}")


async def setup(bot):
    await bot.add_cog(PinnedMessageCog(bot))
