import discord

from utils.park_data import get_ride
from utils.park_data import park_id_to_name


def add_tracked_rides(embed: discord.Embed, rides):
    for ride in rides:
        ride_data = get_ride(ride[1], ride[2])

        embed.add_field(
            name=f"{ride_data['name']} - {park_id_to_name(ride[1])}",
            value=f"**Wait Threshold**: **{ride[3]}** minutes\n" +
                  (f"**Wait Time**: **" + str(ride_data['wait_time']) + 
                   "** minutes\n" if ride_data['is_open'] else "") +
                  "**Status**: " +
                  ("Open\n" if ride_data['is_open'] else "Closed\n") +
                  f"**ID**: {ride[2]}",
            inline=False
        )
