"""Memes cog for SriteBot"""

# Import discord.py and commands extension
import discord
from discord.ext import commands


class Memes(commands.Cog):
    """Memes cog"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.group(description="follow with a specific meme")
    async def meme(self, ctx: commands.Context) -> None:
        """Meme command group"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Specify a meme")

    @meme.command(description="dot dab")
    async def dab(self, ctx: commands.Context) -> None:
        """Dab meme command"""
        await ctx.send(file=discord.File("resources/dab.jpg"))

    @meme.command(description="doge")
    async def angery(self, ctx: commands.Context) -> None:
        """Angery meme command"""
        await ctx.send(
            "https://cdn.discordapp.com/attachments/32440271559"
            + "5767809/353676898892775424/angerydoge.jpg"
        )

    @meme.command(description="laser")
    async def notyet(self, ctx: commands.Context) -> None:
        """Notyet meme command"""
        await ctx.send(
            "https://cdn.discordapp.com/attachments/32440271559"
            + "5767809/353676953800278016/NotYet.png"
        )

    @meme.command(description="yoda")
    async def seagulls(self, ctx: commands.Context) -> None:
        """Seagulls meme command"""
        await ctx.send("https://www.youtube.com/watch?v=U9t-slLl30E")

    @meme.command(description="sun")
    async def angeryr(self, ctx: commands.Context) -> None:
        """Angeryr meme command"""
        await ctx.send(
            "https://www.shitpostbot.com/img/"
            + "sourceimages/angry-doog-angery-57b3a3af935ed.jpeg"
        )

    @meme.command(description="glasses")
    async def putin(self, ctx: commands.Context) -> None:
        """Putin meme command"""
        await ctx.send(
            "https://cdn.discordapp.com/attachments/185587784218574848/"
            + "381346915498983435/Funny-Russia-Meme-20.png"
        )

    @meme.command(description="james")
    async def triger(self, ctx: commands.Context) -> None:
        """Triger meme command"""
        await ctx.send(
            "https://cdn.discordapp.com/attachments/185587784218574848/"
            + "381347025561714690/trgdd_james.png"
        )

    @meme.command()
    async def crusade(self, ctx: commands.Context) -> None:
        """Crusade meme command"""
        await ctx.send(
            "https://cdn.discordapp.com/attachments/271124181372895242/"
            + "463186200618860546/Z.png"
        )


# Setup function to add cog
def setup(bot: commands.Bot) -> None:
    """Loads memes cog"""
    bot.add_cog(Memes(bot))
