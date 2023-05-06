import discord
from discord import app_commands

from utils.park_data import get_park_data
import utils.default_embed as default_embed
from utils.search_images import search_images


def add_ride_status(embed: discord.Embed, ride: dict):
    embed.add_field(
        name=ride['name'],
        value=((f"**Wait Time**: **{ride['wait_time']}** minutes\n"
                if ride['is_open'] else "") +
               ("**Status**: " +
                f"{'Open' if ride['is_open'] else 'Closed'}\n") +
               f"**ID**: {ride['id']}\n"),
        inline=False
    )


async def list_rides(interaction: discord.Interaction,
                     provided_park: app_commands.Choice[int],
                     provided_land: str = None):
    await interaction.response.defer()

    park = get_park_data(provided_park.value)

    embeds = []

    if provided_land is not None:
        lands_to_display = tuple(
            land for land in park['lands'] if
            land['name'].lower() == provided_land.lower()
        )
        if not lands_to_display:
            if (provided_land.lower() == "other"):
                lands_to_display = ()
            else:
                return await interaction.followup.send(
                    f"Could not find land named **{provided_land}.**"
                )
    else:
        lands_to_display = park['lands']

    for land in lands_to_display:
        embed = default_embed.new_embed(land['name'])

        # Search for an image of the ride and add it to the embed
        try:
            embed.set_thumbnail(
                url=search_images(land['name'] + " disneyland california")
            )
        except Exception:
            default_embed.set_default_thumbnail(embed, provided_park.value)
            embed.set_footer(text="Note: Daily image search limit reached.")

        for ride in land['rides']:
            add_ride_status(embed, ride)

        embeds.append(embed)

    if ((not lands_to_display) or lands_to_display == park['lands'] and
                park['rides']):
        embed = default_embed.new_embed("Other Attractions")
        default_embed.set_default_thumbnail(embed, provided_park.value)

        for ride in park['rides']:
            add_ride_status(embed, ride)

        embeds.append(embed)

    await interaction.followup.send(embeds=embeds)
