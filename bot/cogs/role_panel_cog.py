import discord
from discord.ext import commands

from bot.services.role_service import create_role_panel
from bot.utils.db import save_role_panel


class RolePanelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rolepanel")
    async def rolepanel(self, ctx: commands.Context, role_name: str = "member"):
        message, role = await create_role_panel(ctx.channel, role_name)
        save_role_panel(
            guild_id=str(ctx.guild.id),
            channel_id=str(ctx.channel.id),
            message_id=str(message.id),
            role_name=role.name,
            role_id=str(role.id),
        )
        await ctx.send(f"ロールパネルを作成しました: {message.jump_url}")


async def setup(bot):
    await bot.add_cog(RolePanelCog(bot))
