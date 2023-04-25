import os

import discord
from discord import app_commands
from dotenv import load_dotenv

import constants.constants as constants
from commands.get_attraction import get_attraction
from commands.send_attractions import send_attractions
from commands.sync_commands import sync_commands

# Load the Discord token from the .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
MESSAGE_CHANNEL_ID = os.getenv('MESSAGE_CHANNEL_ID')

# The guild and channel to send messages to
GUILD = discord.Object(int(GUILD_ID))
MESSAGE_CHANNEL = discord.Object(int(MESSAGE_CHANNEL_ID))

# Set up the Discord client and command tree
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# Sync command
# ----------
@tree.command(guild=GUILD, description="Sync the commands to the guild.")
async def sync(interaction: discord.Interaction):
    await sync_commands(interaction, tree, GUILD)


# get_attraction commands
# ----------
get_attraction_group = app_commands.Group(
    name="get_attraction", description="Get information about an attraction."
)


# Decorator to add the park choices to the get_attraction commands
def add_park_choices(func):
    func = app_commands.describe(park="The park the attraction is in.")(func)
    func = app_commands.choices(park=constants.PARK_AND_ID_CHOICES)(func)
    return func


# By name
@get_attraction_group.command(
        description="Get information about an attraction by name.")
@app_commands.describe(attraction_name="The name of the attraction.")
@add_park_choices
async def by_name(interaction: discord.Interaction,
                  park: app_commands.Choice[int], attraction_name: str):
    await get_attraction(interaction, park, attraction_name)


# By ID
@get_attraction_group.command(
        description="Get information about an attraction by ID.")
@app_commands.describe(attraction_id="The ID of the attraction.")
@add_park_choices
async def by_id(interaction: discord.Interaction,
                park: app_commands.Choice[int], attraction_id: int):
    await get_attraction(interaction, park, ride_id=attraction_id)


# Add the get_attraction commands to the command tree
tree.add_command(get_attraction_group, guild=GUILD)


# List attractions command
# ----------
@tree.command(guild=GUILD, description="List all attraction names with IDs.")
@add_park_choices
@app_commands.describe(
    land="Optional: Filter by land or specify \"other\" " +
         "to get attractions not in a land. "
)
async def list_attractions(interaction: discord.Interaction,
                           park: app_commands.Choice[int], land: str = None):
    await send_attractions(interaction, park, land)


# Events
# ----------
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
# TODO: Ping if a ride gets shutdown or reopens
