import discord

import utils.park_data as park_data

def add_tracked_rides(embed: discord.Embed, tracked_rides):
    for tracked_ride in tracked_rides:
        park_name = park_data.park_id_to_name(tracked_ride[1])
        ride_is_open = park_data.is_ride_open(tracked_ride[1], tracked_ride[2])

        embed.add_field(
            name=park_data.ride_id_to_name(tracked_ride[1], tracked_ride[2]),
            value=f"**Wait Threshold**: **{tracked_ride[3]}** minutes\n" +
                  f"**Park**: {park_name}\n" +
                  f"**ID**: {tracked_ride[2]}\n" +
                  "**Status**: " +
                  ("Open\n" if ride_is_open else "Closed\n") +
                  ("**Wait Time**: **" +
                   str(park_data.get_ride_wait_time(
                       tracked_ride[1], tracked_ride[2]
                   )) + "** minutes" if
                   ride_is_open else ""),
            inline=False
        )