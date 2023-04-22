import discord
from discord import app_commands


async def sync_commands(interaction: discord.Interaction,
                        tree: app_commands.CommandTree, guild: discord.Object):
    await interaction.response.send_message("Syncing commands...")
    await tree.sync(guild=guild)
    message = await interaction.original_response()
    await message.edit(content="Synced commands!")
