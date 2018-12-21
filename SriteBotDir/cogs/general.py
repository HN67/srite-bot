# General commands cog for SriteBot
import discord
from discord.ext import commands

# Cog class
class General:

    # Init to reference bot
    def __init__(self, bot):
        self.bot = bot

    # Greeting command    
    @commands.command(short="Greets the bot", description="Gets the bot to reply with Hello,"
                                                     + "and is used to test a variety of things on backend")
    async def hello(self, ctx):
        '''Replies with simple text'''
        try:
            await ctx.send("Hi " + ctx.author.nick)
        except TypeError:
            await ctx.send("Hi " + ctx.author.name)
        debug_info("Greeted user", ctx.author.id)

    # Eightball command
    @commands.command(description="Returns yes or no")
    async def eight(self, ctx):
        '''Shakes a magic eight ball'''
        # Store options for response in tuple
        options = ("yes","no","absolutely","maybe","hardly","sure","never")
        # Respond with random option using .choice
        await ctx.send(random.choice(options))

    @commands.command(description="o o o")
    async def echo(self, ctx, amount: int, *, message: str):
        """o o o"""
        if await check_bans(ctx):
            for i in range(amount):
                await ctx.send(message)

    # Echo command
    @echo.error
    async def echo_handler(self, ctx, error):
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send("Please use whole numbers")
        else:
            print("Unexpected error: ")
            print(error)

# Setup function to load cog
def setup(bot):
    bot.add_cog(General(bot))
