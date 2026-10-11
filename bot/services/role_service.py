import discord


async def add_role(member: discord.Member, role: discord.Role):
    if role not in member.roles:
        await member.add_roles(role)


async def remove_role(member: discord.Member, role: discord.Role):
    if role in member.roles:
        await member.remove_roles(role)


async def create_role_panel(channel: discord.TextChannel, role_name: str):
    role = discord.utils.get(channel.guild.roles, name=role_name)
    if role is None:
        role = await channel.guild.create_role(name=role_name)

    view = discord.ui.View(timeout=None)

    async def toggle_role(interaction: discord.Interaction):
        member = interaction.user
        if member is None:
            return
        if role in member.roles:
            await remove_role(member, role)
            await interaction.response.send_message(f"{role.name} ロールを外しました。", ephemeral=True)
        else:
            await add_role(member, role)
            await interaction.response.send_message(f"{role.name} ロールを付与しました。", ephemeral=True)

    button = discord.ui.Button(label=role_name, style=discord.ButtonStyle.primary)
    button.callback = toggle_role
    view.add_item(button)

    embed = discord.Embed(
        title="ロールパネル",
        description=f"{role.name} を付与/削除するにはボタンを押してください。",
        color=discord.Color.blue(),
    )
    message = await channel.send(embed=embed, view=view)
    return message, role
