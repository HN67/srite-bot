"""Moderation tools cog"""

# Import discord
import discord
from discord.ext import commands

# Import core
import core


class Moderation(commands.Cog):
    """SriteBot Moderation tools cog"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prune(self, ctx: commands.Context, number: int) -> None:
        """Prunes messages from the channel"""
        core.debug_info("Running prune command")
        channel: discord.TextChannel = ctx.channel
        async for message in channel.history(limit=number, before=ctx.message):
            await message.delete()
        await core.srite_send(ctx, f"Successfully pruned {number} messages")

    @prune.error
    async def prune_handler(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """Error handler for prune command"""
        core.debug_info("Running prune handler", error)
        if isinstance(error, commands.MissingRequiredArgument):
            await core.srite_send(ctx, "Specify the number of messages to prune. use *prune <num>")
        if isinstance(error, commands.BadArgument):
            await core.srite_send(
                ctx, "Specify the number of messages to prune as a number. use *prune <num>"
            )
        elif isinstance(error, commands.MissingPermissions):
            await core.srite_send(ctx, "Must be an admin to use this command. Nice try.")


# Function to add cog
def setup(bot: commands.Bot) -> None:
    """Loads moderal cog"""
    bot.add_cog(Moderation(bot))
