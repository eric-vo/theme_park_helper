import discord
from discord import app_commands

import utils.default_embed as default_embed
from utils.park_data import get_park_data
from utils.search_images import search_images


async def check_and_message(interaction: discord.Interaction,
                            park: app_commands.Choice[int],
                            provided_ride: dict, desired_ride_name: str,
                            desired_ride_id: int, land=None):
    """Compares a provided ride to a desired ride name or ID
    and sends the ride's status message if they match.
    Only provide either name or iD.

    Parameters
    ----------
    interaction : discord.Interaction
        The interaction to respond to
    park : app_commands.Choice[int]
        The park the provided ride is in
    ride : str
        The ride to compare to the desired ride
    desired_ride_name : str
        The desired ride name
    desired_ride_id : int
        The desired ride ID
    land : _type_, optional
        The land the provided ride is in, by default None

    Returns
    -------
    bool
        If the provided ride matches the desired ride and a message was sent
    """

    # If the ride name or ID matches the desired ride name or ID
    if ((desired_ride_name is not None and
            provided_ride['name'].lower() == desired_ride_name.lower()) or
            provided_ride['id'] == desired_ride_id):
        # Initialize the embed
        embed = default_embed.new_embed(provided_ride['name'])
        default_embed.set_default_thumbnail(embed, park.value)
        embed.add_field(name="ID", value=provided_ride['id'], inline=False)
        embed.add_field(name="Park", value=park.name, inline=False)

        # If the ride is in a land, add the land to the embed
        if land:
            embed.add_field(name="Land", value=land, inline=False)

        # If the ride is open, add the wait time to the embed
        # Otherwise, add that the ride is closed
        if provided_ride['is_open']:
            embed.add_field(name="Status", value="Open", inline=False)
            embed.add_field(
                name="Wait Time",
                value=f"**{provided_ride['wait_time']}** minutes",
                inline=False
            )
        else:
            embed.add_field(name="Status", value="Closed")

        try:
            embed.set_image(
                url=search_images(provided_ride['name'] +
                                  " disneyland california")
            )
        except Exception:
            embed.set_footer(text="Note: Daily image search limit reached.")

        # Send the embed
        await interaction.response.send_message(embed=embed)
        return True


async def get_ride(interaction: discord.Interaction,
                   park: app_commands.Choice[int],
                   ride_name: str = None, ride_id: int = None):
    """Looks for an attraction with the provided name or ID
    and sends its status message if it exists. Only provide either name or ID.

    Parameters
    ----------
    interaction : discord.Interaction
        The interaction to respond to
    park_id : int
        The park_id to look for the attraction in
    ride_name : str, optional
        The desired attraction name, by default None
    ride_id : int, optional
        The desired attraction ID, by default None
    """

    # Get the attractions' data from the Queue-Times API
    park_data = get_park_data(park.value)

    # Check if the desired ride is in the list of rides that aren't in a land
    for ride in park_data['rides']:
        if await check_and_message(interaction, park,
                                   ride, ride_name, ride_id):
            return

    # Check if the desired ride is in the list of rides that are in a land
    for land in park_data['lands']:
        for ride in land['rides']:
            if await check_and_message(interaction, park, ride,
                                       ride_name, ride_id, land['name']):
                return

    # If the desired ride wasn't found, send an error message
    await interaction.response.send_message(
        "Could not find an attraction " +
        (f"named **{ride_name}**." if ride_name else f"with ID **{ride_id}**.")
    )
