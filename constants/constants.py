import discord
from discord import app_commands

PARK_AND_ID_CHOICES = [
    app_commands.Choice(name="Disneyland Park", value=16),
    app_commands.Choice(name="Disney California Adventure", value=17),
    app_commands.Choice(name="Universal Studios Hollywood", value=66)
]

DEFAULT_EMBED = {
    'description': ("[Powered by Queue-Times.com]" +
                    "(https://queue-times.com/en-US)"),
    'color': discord.Color.og_blurple(),
    16: "https://is.gd/ZKNQZ9",
    17: "https://is.gd/D6ajuW",
    66: "https://is.gd/B1gxxo"
}
