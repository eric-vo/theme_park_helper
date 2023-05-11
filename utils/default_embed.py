import discord

from constants.constants import DEFAULT_EMBED


def new_embed(title: str, description: str = DEFAULT_EMBED['description'],
              color=DEFAULT_EMBED['color']) -> discord.Embed:
    return discord.Embed(title=title, description=description, color=color)


def set_default_thumbnail(embed: discord.Embed, park_id: int):
    embed.set_thumbnail(
        url=(DEFAULT_EMBED[park_id])
    )
