import discord
from discord import app_commands


async def sync_commands(interaction: discord.Interaction,
                        tree: app_commands.CommandTree, guild: discord.Object):
    """Syncs the commands in the command tree to the guild.

    Parameters
    ----------
    interaction : discord.Interaction
        The interaction to respond to
    tree : app_commands.CommandTree
        The command tree to sync
    guild : discord.Object
        The guild to sync the commands to
    """
    await interaction.response.defer()
    await tree.sync(guild=guild)
    await interaction.followup.send(content="Synced commands!")
