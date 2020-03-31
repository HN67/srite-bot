"""April fools cog"""

# Import python core modules

# Import discord.py
import discord
from discord.ext import commands

# Import custom modules
import config


class Fools(commands.Cog):
    """SriteBot Fools Cog"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Checks messages to perform april fools logic"""
        if not message.author.id == self.bot.user.id:
            # Get context
            ctx: commands.Context = await self.bot.get_context(message)
            # Check if in a valid channel
            if ctx.channel.id in config.fools.channels:
                # Delete the original message
                await ctx.message.delete()
                # Prepare the embed
                embed: discord.Embed = discord.Embed(
                    color=config.bot.color,  # Embed color on the side
                    # title="Social Distance Relay",
                    description=ctx.message.content,  # Embed main content
                    timestamp=ctx.message.created_at,
                )
                embed.set_author(
                    name=ctx.author.display_name,
                    icon_url=ctx.author.avatar_url,
                )
                embed.set_footer(text="Social Distance Relay")
                # Send the embed
                await ctx.send(embed=embed)


# Function to add cog
def setup(bot: commands.Bot) -> None:
    """Loads fools cog"""
    bot.add_cog(Fools(bot))
