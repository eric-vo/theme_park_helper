import discord
from discord import app_commands
import sqlite3

import database.database as db
from utils.default_embed import new_embed
import utils.park_data as park_data
from utils.search_images import search_images
from utils.tracking_embed import add_tracked_rides


# TODO: Speed this up
async def track_ride(interaction: discord.Interaction,
                     park: app_commands.Choice[int], wait_threshold: int,
                     ride_name: str = None, ride_id: int = None):
    await interaction.response.defer()
    
    try:
        if (len(db.select_rides(interaction.user.id)) >= 25):
            return await interaction.followup.send(
                "You have reached the maximum number of tracked rides. " +
                "Please remove some rides before adding more."
            )
    except sqlite3.OperationalError:
        db.create_table()

    if ride_name is not None:
        ride_id = park_data.ride_name_to_id(park.value, ride_name)
        if ride_id is None:
            return await interaction.followup.send(
                f"Ride with name **{ride_name}** not found.")
    else:
        ride_name = park_data.ride_id_to_name(park.value, ride_id)
        if ride_name is None:
            return await interaction.followup.send(
                f"Ride with ID **{ride_id}** not found.")
        
    db.insert_ride(interaction.user.id, park.value,
                   ride_id, wait_threshold)
    
    tracked_rides = db.select_rides(interaction.user.id)
    embed = new_embed(
        f"Tracking {ride_name.title()}!",
        "Here are your current tracked rides:"
    )
    embed.set_image(
        url=search_images(f"{ride_name} disneyland california")
    )

    add_tracked_rides(embed, tracked_rides)
    
    await interaction.followup.send(embed=embed)