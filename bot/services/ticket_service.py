import discord

from bot.utils.db import get_connection, get_next_ticket_number


async def create_ticket(guild: discord.Guild, owner: discord.Member):
    ticket_number = get_next_ticket_number()

    category = discord.utils.get(guild.categories, name="Tickets")
    if category is None:
        category = await guild.create_category("Tickets")

    channel = await guild.create_text_channel(
        f"ticket-{ticket_number}",
        category=category,
        overwrites={
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            owner: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                read_messages=True,
            ),
        },
    )

    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO tickets (ticket_number, user_id, guild_id, channel_id, status)
            VALUES (?, ?, ?, ?, 'open')
            """,
            (ticket_number, str(owner.id), str(guild.id), str(channel.id)),
        )
        conn.commit()
    finally:
        conn.close()

    return ticket_number, channel
