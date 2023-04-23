import discord
from discord import app_commands

PARK_AND_ID_CHOICES = [
    app_commands.Choice(name="Disneyland Park", value=16),
    app_commands.Choice(name="Disney California Adventure", value=17)
]

DEFAULT_EMBED = {
    'description': ("[Powered by Queue-Times.com]" +
                    "(https://queue-times.com/en-US)"),
    'color': discord.Color.og_blurple(),
    'disneyland_logo': "https://is.gd/ZKNQZ9",
    'disney_ca_logo': "https://is.gd/D6ajuW"
}
