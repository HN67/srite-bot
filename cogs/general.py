"""General commands cog for SriteBot"""

# Import core libraries
import random

# Import discord.py
import discord
from discord.ext import commands

# Import core
import core


# Cog class
class General(commands.Cog):
    """SriteBot General Cog"""

    # Init to reference bot
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # Greeting command
    @commands.command(
        short="Greets the bot",
        description="Gets the bot to reply with Hello,"
        + "and is used to test a variety of things on backend",
    )
    async def hello(self, ctx: commands.Context) -> None:
        """Replies with simple text"""
        await ctx.send("Hi " + ctx.author.display_name)
        core.debug_info("Greeted user", ctx.author.id)

    # Eightball command
    @commands.command(description="Returns yes or no")
    async def eight(self, ctx: commands.Context) -> None:
        """Shakes a magic eight ball"""
        # Store options for response in tuple
        options = ("yes", "no", "absolutely", "maybe", "hardly", "sure", "never")
        # Respond with random option using .choice
        await ctx.send(random.choice(options))

    @commands.command(description="o o o")
    async def echo(self, ctx: commands.Context, amount: int, *, message: str) -> None:
        """o o o"""
        for _ in range(amount):
            await ctx.send(message)

    # Echo command
    @echo.error
    async def echo_handler(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Error handler for echo command"""
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send("Please use whole numbers")
        else:
            print("Unexpected error: ")
            print(error)

    @commands.command(description="Mocks the message sent directly before this command")
    async def mock(self, ctx: commands.Context) -> None:
        """Mocks previous message"""
        # Get previous message
        previous: discord.Message = (await ctx.channel.history(limit=2).flatten())[1]
        # ReSend the content but mocked
        await ctx.send(
            "".join(
                random.choice((char.upper, char.lower))() for char in previous.content
            )
        )

    @commands.command(description="Bans the target user")
    async def ban(self, ctx: commands.Context, member: discord.Member) -> None:
        """Bans someone"""
        await core.srite_send(ctx, f"*{member.mention} has been banned.* Cya!")

    # Open console command
    @commands.command(hidden=True)
    @commands.is_owner()
    async def console(self, ctx: commands.Context) -> None:
        """Opens the console to input, only available to HN67"""
        await ctx.message.delete()
        temp = input("Request for console input: ")
        await ctx.send(temp)

    # On message event
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Event callback for on message handling"""

        # Make sure author is not SriteBot (prevent loops)
        if message.author.id != 348653600345423873:

            # Relable message content
            text = message.content.lower()
            # Relable channel
            channel = message.channel

            # Search for certain phrases
            # if "im " in text:
            #     await channel.send(
            #         "hi {0}, im SriteBot.".format(text[text.find("im") + 2 :].strip())
            #     )


# Setup function to load cog
def setup(bot: commands.Bot) -> None:
    """Loads general cog"""
    bot.add_cog(General(bot))
