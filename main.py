import os
# import sqlite3
import time

import discord
from discord import app_commands
from dotenv import load_dotenv

import constants.constants as constants
from commands.get_ride import get_ride
from commands.list_rides import list_rides
from commands.sync_commands import sync_commands
from commands.track_ride import track_ride

# Connect to ride tracking database
# connection = sqlite3.connect("ride_tracker.db")

# cursor = connection.cursor()

# Create a table that holds a user's ID and the attractions they are tracking
# cursor.execute("""CREATE TABLE users (
#                    user_id integer,
#                    park_id integer,
#                    ride_id integer,
#                    wait_threshold integer
#                )""")

# cursor.execute("INSERT INTO users VALUES (123, 456, 789)")

# connection.commit()

# cursor.execute("INSERT INTO users VALUES (?, ?, ?)",
#   (user_id, park_id, ride_id))

# connection.commit()

# cursor.execute("INSERT INTO users VALUES (:user_id, :ride_id, :park_id)",
#   {'user_id': user_id, 'ride_id': ride_id, 'park_id': park_id})

# connection.commit()

# cursor.execute("SELECT * FROM users WHERE user_id = 123")
# cursor.execute("SELECT * FROM users WHERE user_id=?", (123,))

# print(cursor.fetchall())

# connection.commit()

# connection.close()

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


async def track_rides():
    """Track rides and send messages to the message channel."""
    while True:
        time.sleep(5 * 60)


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
@add_park_choices
@app_commands.describe(attraction_name="The name of the attraction.")
async def by_name(interaction: discord.Interaction,
                  park: app_commands.Choice[int], attraction_name: str):
    await get_ride(interaction, park, attraction_name)


# By ID
@get_attraction_group.command(
        description="Get information about an attraction by ID.")
@add_park_choices
@app_commands.describe(attraction_id="The ID of the attraction.")
async def by_id(interaction: discord.Interaction,
                park: app_commands.Choice[int], attraction_id: int):
    await get_ride(interaction, park, ride_id=attraction_id)


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
    await list_rides(interaction, park, land)


# track_attraction commands
# ----------
track_attraction_group = app_commands.Group(
    name="track_attraction", description="Track an attraction."
)


@track_attraction_group.command(
        description="Track an attraction by name.")
@add_park_choices
@app_commands.describe(attraction_name="The name of the attraction.")
@app_commands.describe(wait_threshold="The wait time threshold in minutes.")
async def by_name(interaction: discord.Interaction,
                  park: app_commands.Choice[int], attraction_name: str,
                  wait_threshold: int):
    await track_ride(interaction, park, wait_threshold, attraction_name)


@track_attraction_group.command(
        description="Track an attraction by ID.")
@add_park_choices
@app_commands.describe(attraction_id="The ID of the attraction.")
@app_commands.describe(wait_threshold="The wait time threshold in minutes.")
async def by_id(interaction: discord.Interaction,
                park: app_commands.Choice[int], attraction_id: int,
                wait_threshold: int):
    await track_ride(interaction, park, wait_threshold, ride_id=attraction_id)


# Add the get_attraction commands to the command tree
tree.add_command(track_attraction_group, guild=GUILD)


# Events
# ----------
@client.event
async def on_ready():
    print(f"Ready! logged in as {client.user}.")
    # track_rides()


client.run(TOKEN)

# TODO: Add command to add attractions with desired wait threshold
# If the attraction is already being tracked, update its wait threshold
# TODO: Add command to remove attractions
# TODO: Add command to list attractions with wait thresholds and times
# TODO: Add command to clear all attractions
# TODO: Add command to toggle tracking of attractions
# TODO: Ping if a ride gets shutdown or reopens
