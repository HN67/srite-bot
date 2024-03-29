"""Timing commands cog for SriteBot"""

# Import core librarys
import asyncio
import datetime
import time

# Import discord.py
import discord
from discord.ext import commands

# Import core
import core

# Import config
import config


# Cog class
class Timing(commands.Cog):
    """SriteBot Timing Cog"""

    # Init to reference bot
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        # Save starting time
        self.start_time = int(time.time())

    # Uptime command
    @commands.command()
    async def uptime(self, ctx: commands.Context) -> None:
        """Returns the uptime of the bot."""
        delta = int(time.time()) - self.start_time
        await core.srite_send(ctx, str(datetime.timedelta(seconds=delta)))

    # Surprise command
    @commands.command()
    async def surprise(
        self, ctx: commands.Context, delay: int, *, message: str
    ) -> None:
        """Echos the message after delay seconds"""
        core.debug_info("Surprise message", message)
        await asyncio.sleep(delay)
        await ctx.send(message)

    @surprise.error
    async def surprise_handler(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Handles surprise command errors"""
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send("Please use whole numbers")
        else:
            print("Unexpected error: ")
            print(error)

    @commands.command()
    async def timer(self, ctx: commands.Context, duration: int) -> None:
        """Displays a counting down timer"""
        # Time remaining
        left = duration
        # Create message
        message = await ctx.send("```Timer: {0}```".format(left))
        # Tick down through qued remaining time, editing message
        while left > 0:
            await message.edit(content="```Timer: {0}```".format(left))
            left -= config.time.interval
            await asyncio.sleep(config.time.interval)
        # Finish the timer message
        await message.edit(content="```Timer: Done```")
        # Mention original command author
        await ctx.send("Timer Finished {0}".format(ctx.author.mention))

    @commands.command(name="time")
    async def _time(self, ctx: commands.Context) -> None:
        """Times how long it takes you to respond with 'stop'"""
        # Save current time
        current = time.time()

        await core.srite_send(ctx.channel, "Waiting for 'stop' within 10s")

        # Define check (what msg to wait for)
        def check(msg: discord.Message) -> bool:
            return (
                msg.content == "stop"
                and msg.channel == ctx.channel
                and msg.author == ctx.author
            )

        # Wait for a response
        try:
            await self.bot.wait_for("message", check=check, timeout=config.time.timeout)

        # Timeout clause
        except asyncio.TimeoutError:
            await ctx.send(
                embed=core.srite_msg(f"Timeout at {config.time.timeout} seconds")
            )

        # Response found
        else:
            # Find change in time
            change = time.time() - current
            # Send msg
            await ctx.send(embed=core.srite_msg(f"Responded in {change} seconds"))


# Function to load cog
def setup(bot: commands.Bot) -> None:
    """Loads timing cog"""
    bot.add_cog(Timing(bot))
