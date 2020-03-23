# Misc cog that contains HN67's scripts command wrappers
import discord
from discord.ext import commands

# Import custom HN67 scripts
from scripts import *

class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Maze command
    @commands.command()
    async def maze(self, ctx, size: int):
        if size <= 30:
            maze = Maze.MazeGenerator(size).generateMap()
            maze[size - 1][size//2].borders["bottom"] = False
            string = Maze.drawMap(maze)
            string = string[:size + 1*(size % 2  == 0)] + " " + string[size + 1 + 1*(size % 2  == 0):]
            await ctx.send("```"+string+"```")
        else:
            await ctx.send("Max maze size is 30")

    @maze.error
    async def maze_handler(self, ctx, error):
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
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send("Please use whole numbers")
        else:
            debug_info("Unexpected error: ",error)

    # Random number generator
    async def rand(ctx, bounds):
        for index in range(len(bounds) - 1):
            result = random.randint(bounds[index], bounds[index + 1])
            await ctx.send("Random number between " + str(bounds[index]) + " and "
                           + str(bounds[index + 1]) + ": " + str(result))

    # Random number generator commands
    @commands.command(name="rand", description="Generates a random number between numbers provided, inclusive")
    async def _rand(self, ctx, *bounds: int):
        '''Generates a random number'''
        await self.rand(ctx, bounds)


    @commands.command(description="Generates random numbers, the first argument is amount of repetetions")
    async def mrand(self, ctx, *bounds: int):
        '''Generates multiple random numbers'''
        if await check_bans(ctx):
            debug_info("Mrand Function activated with  context {0}".format(ctx))
            for i in range(bounds[0]):
                await self.rand(ctx, bounds[1:])


    @_rand.error
    async def rand_handler(self, ctx, error):
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send("Please use whole numbers")
        else:
            print("Unexpected error: ")
            print(error)

# Setup function to add cog
def setup(bot):
    bot.add_cog(Misc(bot))
