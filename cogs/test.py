"""Testing cog for SriteBot"""

import asyncio

# Import discord.py
# import discord
from discord.ext import commands

# Import core
# import core


class Test(commands.Cog):
    """Testing cog for SriteBot.

    Contains commands used for testing / experimenting with internals.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(description="Echos the raw message content.")
    async def recho(self, ctx: commands.Context, *, message: str) -> None:
        """Replies with whatever was sent."""
        await ctx.send(message)


# Boilerplate to load the cog
def setup(bot: commands.Bot) -> None:
    """Loads general cog"""
    bot.add_cog(Test(bot))
