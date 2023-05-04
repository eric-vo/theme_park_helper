import discord
from discord import app_commands

import database.database as db
from utils.park_data import get_park_data

async def track_ride(interaction: discord.Interaction,
                     park: app_commands.Choice[int], wait_threshold: int,
                     ride_name: str = None,
                     ride_id: int = None):
    await interaction.response.defer()

    if ride_name is not None:
        data = get_park_data(park.value)
        
        for land in data['lands']:
            for ride in land['rides']:
                if ride['name'].lower() == ride_name.lower():
                    desired_ride_id = ride['id']
                    break
        else:
            for ride in data['rides']:
                if ride['name'].lower() == ride_name.lower():
                    desired_ride_id = ride['id']
                    break
            else:
                return await interaction.followup.send("Ride not found.")
    else:
        desired_ride_id = ride_id
    db.insert_ride(interaction.user.id, park.value,
                   desired_ride_id, wait_threshold)
    await interaction.followup.send(db.select_rides(interaction.user.id))