# Timing commands cog for SriteBot
import discord
from discord.ext import commands

# Cog class
class Timing:

    # Init to reference bot
    def __init__(self, bot):
        self.bot = bot

        # Tick Interval for timer command
        self.interval = 1

    # Surprise command
    @commands.command()
    async def surprise(ctx, delay: int, *, message: str):
        '''Echos the message after delay seconds'''
        debug_info("Surprise message",message)
        await asyncio.sleep(delay)
        await ctx.send(message)

    @surprise.error
    async def surprise_handler(ctx, error):
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send("Please use whole numbers")
        else:
            print("Unexpected error: ")
            print(error)

    @commands.command()
    async def timer(ctx, duration: int):
        """Displays a counting down timer"""
        # Time remaining
        left = duration
        # Create message
        message = await ctx.send("```Timer: {0}```".format(left))
        # Tick down through qued remaining time, editing message
        while left > 0:
            await message.edit(content = "```Timer: {0}```".format(left))
            left -= self.interval
            await asyncio.sleep(self.interval)
        # Finish the timer message
        await message.edit(content = "```Timer: Done```")
        # Mention original command author
        await ctx.send("Timer Finished {0}".format(ctx.author.mention))

    
# Function to load cog
def setup(bot):
    bot.add_cog(Timing(bot))
