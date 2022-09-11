"""Misc cog that contains HN67's scripts command wrappers"""

# Import python modules
import random

# Import discord.py
import discord
from discord.ext import commands

# Import custom HN67 scripts
from scripts import Maze
from scripts import AltChain
from scripts import Spam

# Import core
import core


class Misc(commands.Cog):
    """SriteBot Misc Cog"""

    def __init__(self, bot):
        self.bot = bot

    # Maze command
    @commands.command()
    async def maze(self, ctx, size: int):
        """Generates a maze"""
        if size <= 30:
            maze = Maze.MazeGenerator(size).generateMap()
            maze[size - 1][size // 2].borders["bottom"] = False
            string = Maze.drawMap(maze)
            string = (
                string[: size + 1 * (size % 2 == 0)]
                + " "
                + string[size + 1 + 1 * (size % 2 == 0) :]
            )
            await ctx.send("```" + string + "```")
        else:
            await ctx.send("Max maze size is 30")

    @maze.error
    async def maze_handler(self, ctx, error):
        """Handles maze command errors"""
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send("Please use whole numbers")
        else:
            print("Unexpected error: ")
            print(error)

    # Random fact (xkcd) command
    @commands.command()
    async def fact(self, ctx):
        """Displays a random calendar fact"""
        await ctx.send(AltChain.xkcd.value())

    # Spam command
    @commands.command()
    async def spam(self, ctx, length: int):
        """Displays a paragraph from the spam module"""
        await ctx.send(Spam.paragraph(length))

    @spam.error
    async def spam_handler(self, ctx, error):
        """Handles spam command errors"""
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send("Please use whole numbers")
        else:
            core.debug_info("Unexpected error: ", error)

    # Random number generator
    async def rand(self, ctx, bounds):
        """Generates a random number, and sends the result as a message"""
        for index in range(len(bounds) - 1):
            result = random.randint(bounds[index], bounds[index + 1])
            await ctx.send(
                "Random number between "
                + str(bounds[index])
                + " and "
                + str(bounds[index + 1])
                + ": "
                + str(result)
            )

    # Random number generator commands
    @commands.command(
        name="rand",
        description="Generates a random number between numbers provided, inclusive",
    )
    async def _rand(self, ctx, *bounds: int):
        """Generates a random number"""
        await self.rand(ctx, bounds)

    @commands.command(
        description="Generates random numbers, the first argument is amount of repetetions"
    )
    async def mrand(self, ctx, *bounds: int):
        """Generates multiple random numbers"""
        core.debug_info("Mrand Function activated with  context {0}".format(ctx))
        for dummy in range(bounds[0]):
            await self.rand(ctx, bounds[1:])

    @_rand.error
    async def rand_handler(self, ctx, error):
        """Handles rand command errors"""
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send("Please use whole numbers")
        else:
            print("Unexpected error: ")
            print(error)


# Setup function to add cog
def setup(bot):
    """Loads misc cog"""
    bot.add_cog(Misc(bot))
