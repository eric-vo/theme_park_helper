import asyncio
import os
import sqlite3

import discord
from discord import app_commands
from dotenv import load_dotenv
from commands.get_tracked_rides import get_tracked_rides
from commands.untrack_ride import untrack_ride

import constants.constants as constants
from commands.get_ride import get_ride
from commands.list_rides import list_rides
from commands.sync_commands import sync_commands
from commands.track_ride import track_ride
import database.database as db
from utils.default_embed import new_embed, set_default_thumbnail
import utils.park_data as park_data
from utils.search_images import search_images

# Load the Discord token from the .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
MESSAGE_CHANNEL_ID = os.getenv('MESSAGE_CHANNEL_ID')

# The guild and channel to send messages to
GUILD = discord.Object(int(GUILD_ID))

# Set up the Discord client and command tree
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

TRACKING_INTERVAL = 2 * 60


async def track_rides():
    """Track rides and send messages to the message channel."""
    while True:
        try:
            tracked_rides = db.select_rides()
        except sqlite3.OperationalError:
            db.create_table()
            continue

        for ride in tracked_rides:
            user_id, park_id, ride_id, wait_threshold, reached_threshold = ride
            wait_time = park_data.get_ride_wait_time(park_id, ride_id)
            
            if wait_time is None:
                continue
            
            print(wait_time, wait_threshold, reached_threshold)
            
            if wait_time <= wait_threshold and not reached_threshold:
                ride_name = park_data.ride_id_to_name(park_id, ride_id)
                embed = new_embed(
                    "New update!",
                    f"**{ride_name}** has now reached your wait threshold."
                )
                set_default_thumbnail(embed, park_id)
                embed.set_image(
                    url=search_images(f"{ride_name} disneyland california")
                )
                embed.add_field(
                    name="Wait Threshold",
                    value=f"**{wait_threshold}** minutes",
                )
                embed.add_field(
                    name="Wait Time",
                    value=f"**{wait_time}** minutes",
                )

                db.update_reached_threshold(user_id, park_id, ride_id, 1)
                
                channel = client.get_channel(int(MESSAGE_CHANNEL_ID))
                await channel.send(content=f"<@{user_id}>", embed=embed)
            elif wait_time > wait_threshold and reached_threshold:
                ride_name = park_data.ride_id_to_name(park_id, ride_id)
                embed = new_embed(
                    "New update!",
                    f"**{ride_name}** is now above your wait threshold."
                )
                set_default_thumbnail(embed, park_id)
                embed.set_image(
                    url=search_images(f"{ride_name} disneyland california")
                )
                embed.add_field(
                    name="Wait Threshold",
                    value=f"**{wait_threshold}** minutes",
                )
                embed.add_field(
                    name="Wait Time",
                    value=f"**{wait_time}** minutes",
                )

                db.update_reached_threshold(user_id, park_id, ride_id, 0)
                
                channel = client.get_channel(int(MESSAGE_CHANNEL_ID))
                await channel.send(content=f"<@{user_id}>", embed=embed)
            
            
        await asyncio.sleep(TRACKING_INTERVAL)


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


# untrack_attraction commands
# ----------
untrack_attraction_group = app_commands.Group(
    name="untrack_attraction", description="Untrack an attraction."
)


@untrack_attraction_group.command(
        description="Untrack an attraction by name.")
@add_park_choices
@app_commands.describe(attraction_name="The name of the attraction.")
async def by_name(interaction: discord.Interaction,
                          park: app_commands.Choice[int],
                          attraction_name: str):
    await untrack_ride(interaction, park, attraction_name)
    
    
@untrack_attraction_group.command(
        description="Untrack an attraction by ID.")
@add_park_choices
@app_commands.describe(attraction_id="The ID of the attraction.")
async def by_id(interaction: discord.Interaction,
                        park: app_commands.Choice[int],
                        attraction_id: int):
    await untrack_ride(interaction, park, ride_id=attraction_id)


# Add the get_attraction commands to the command tree
tree.add_command(untrack_attraction_group, guild=GUILD)


@tree.command(guild=GUILD, description="List all tracked attractions.")
async def get_tracked_attractions(interaction: discord.Interaction):
    await get_tracked_rides(interaction)


# Events
# ----------
@client.event
async def on_ready():
    print(f"Ready! logged in as {client.user}.")
    await track_rides()


client.run(TOKEN)

# TODO: Add command to clear all attractions
# TODO: Ping if a ride gets shutdown or reopens
