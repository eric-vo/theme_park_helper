import os

from dotenv import load_dotenv
import requests
import discord
from google_images_search import GoogleImagesSearch

load_dotenv()
GCS_DEV_KEY = os.getenv('GCS_DEV_KEY')
GCS_CX = os.getenv('GCS_CX')

gis = GoogleImagesSearch(GCS_DEV_KEY, GCS_CX)
search_params = {
    'num': 1,
    'fileType': 'jpg|gif|png',
    'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|' +
              'cc_noncommercial|cc_nonderived'
}


async def check_and_message(
        interaction: discord.Interaction, ride: str,
        desired_ride_name: str, land=None):
    if ride['name'].lower() == desired_ride_name.lower():
        embed = discord.Embed(
            title=ride['name'],
            description="[Powered by Queue-Times.com]" +
                        "(https://queue-times.com/en-US)",
            color=0x0C71B9
        )
        embed.set_thumbnail(
            url="https://fontmeme.com/images/Disneyland-Park-Logo.jpg"
        )

        if land:
            embed.add_field(name="Land", value=land, inline=False)

        if ride['is_open']:
            embed.add_field(name="Status", value="Open", inline=False)
            embed.add_field(name="Wait Time",
                            value=f"**{ride['wait_time']}** minutes",
                            inline=False)
        else:
            embed.add_field(name="Status", value="Closed")

        search_params['q'] = ride['name'] + " disneyland california"
        gis.search(search_params=search_params)

        for image in gis.results():
            embed.set_image(url=image.url)
            break

        await interaction.response.send_message(embed=embed)
        return True


async def get_attraction(
        interaction: discord.Interaction, ride_name: str):
    response_json = requests.get(
        'https://queue-times.com/en-US/parks/16/queue_times.json'
    ).json()
    # print(json.dumps(response.json(), sort_keys=True, indent=4))

    for ride in response_json['rides']:
        if await check_and_message(interaction, ride, ride_name):
            return

    for land in response_json['lands']:
        for ride in land['rides']:
            if await check_and_message(
                    interaction, ride, ride_name, land['name']):
                return

    await interaction.response.send_message(
        f"Could not find an attraction named **{ride_name}.**"
    )
