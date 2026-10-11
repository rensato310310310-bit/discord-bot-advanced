import discord


async def send_pinned_message(channel: discord.TextChannel, content: str):
    message = await channel.send(content)
    await message.pin()
    return message


async def update_pinned_message(channel: discord.TextChannel, content: str):
    async for message in channel.history(limit=20):
        if message.pinned:
            await message.edit(content=content)
            return message
    return await send_pinned_message(channel, content)
