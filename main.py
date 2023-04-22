import os

from dotenv import load_dotenv
import discord
from discord import app_commands

import commands.sync_commands
import commands.get_attraction

TIME_INTERVAL = 5  # Minutes

GUILD = discord.Object(1061535389598363648)
MESSAGE_CHANNEL = discord.Object(1061535390542086286)

# Load the Discord token from the .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Set up the Discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# Commands
@tree.command(guild=GUILD)
async def sync(interaction: discord.Interaction):
    await commands.sync_commands.sync_commands(interaction, tree, GUILD)


@tree.command(guild=GUILD)
async def get_attraction_by_name(
        interaction: discord.Interaction, attraction_name: str):
    await commands.get_attraction.get_attraction(
        interaction, attraction_name
    )


# Events
@client.event
async def on_ready():
    print(f"Ready! logged in as {client.user}.")


client.run(TOKEN)


# TODO: Add command to add attractions with desired wait threshold
# If the attraction is already being tracked, update its wait threshold
# TODO: Add command to remove attractions
# TODO: Add command to list attractions with wait thresholds and times
# TODO: Add command to clear all attractions
# TODO: Add command to toggle tracking of attractions
