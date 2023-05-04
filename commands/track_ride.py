import discord
from discord import app_commands
import sqlite3

import database.database as db
from utils.default_embed import new_embed
import utils.park_data as park_data

async def track_ride(interaction: discord.Interaction,
                     park: app_commands.Choice[int], wait_threshold: int,
                     ride_name: str = None,
                     ride_id: int = None):
    await interaction.response.defer()
    
    try:
        if (len(db.select_rides(interaction.user.id)) >= 25):
            return await interaction.followup.send(
                "You have reached the maximum number of tracked rides. " +
                "Please remove some rides before adding more.")
    except sqlite3.OperationalError:
        db.create_table()

    if ride_name is not None:
        data = park_data.get_park_data(park.value)
        
        desired_ride_id = None
        
        for land in data['lands']:
            for ride in land['rides']:
                if ride['name'].lower() == ride_name.lower():
                    desired_ride_id = ride['id']
                    break

        if desired_ride_id is None:
            for ride in data['rides']:
                if ride['name'].lower() == ride_name.lower():
                    desired_ride_id = ride['id']
                    break

        if desired_ride_id is None:
            return await interaction.followup.send(
                f"Ride with name **{ride_name}** not found.")
    else:
        desired_ride_id = ride_id
        
    db.insert_ride(interaction.user.id, park.value,
                   desired_ride_id, wait_threshold)
    
    embed = new_embed("Ride added!", "Here are your tracked rides:")
    tracked_rides = db.select_rides(interaction.user.id)
    for tracked_ride in tracked_rides:
        park_name = park_data.park_id_to_name(tracked_ride[1])
        embed.add_field(
            name=park_data.ride_id_to_name(tracked_ride[1], tracked_ride[2]),
            value=f"**Park**: {park_name}\n" +
                  f"**Wait Threshold**: **{tracked_ride[3]}** minutes",
            inline=False
        )
    
    await interaction.followup.send(embed=embed)