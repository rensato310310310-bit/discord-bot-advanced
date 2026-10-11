import discord
from discord.ext import commands

from bot.services.ticket_service import create_ticket


class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ticket")
    async def ticket(self, ctx: commands.Context):
        ticket_number, channel = await create_ticket(ctx.guild, ctx.author)
        await ctx.send(f"チケットを作成しました: {channel.mention} (#{ticket_number})")


async def setup(bot):
    await bot.add_cog(TicketCog(bot))
