import discord
import sqlite3

import database.database as db
from utils.default_embed import new_embed
from utils.tracking_embed import add_tracked_rides


async def get_tracked_rides(interaction: discord.Interaction):
    await interaction.response.defer()
    
    try:
        if (len(db.select_rides(interaction.user.id)) <= 0):
            return await interaction.followup.send(
                "You are not tracking any rides."
            )
    except sqlite3.OperationalError:
        db.create_table()
    
    tracked_rides = db.select_rides(interaction.user.id)
    embed = new_embed(
        "Tracked Rides",
        "Here are your currently tracked rides:"
    )
    
    add_tracked_rides(embed, tracked_rides)
    
    await interaction.followup.send(embed=embed)