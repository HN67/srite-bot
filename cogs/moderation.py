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

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def mod(self, ctx: commands.Context) -> None:
        """Moderation command group"""
        if ctx.invoked_subcommand is None:
            await core.srite_send(ctx, "Please specify a subcommand")

    @mod.error
    async def mod_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Error handler for mod commands"""
        if isinstance(error, commands.MissingPermissions):
            await core.srite_send(
                ctx, "Must be an admin to use this command. Nice try."
            )
        else:
            await core.srite_send(ctx, "There was an unexpected error")
            core.debug_info("Unexpected error in mod command", error)

    @mod.command()
    async def prune(self, ctx: commands.Context, number: int) -> None:
        """Prunes messages from the channel"""
        core.debug_info("Running prune command")
        channel: discord.TextChannel = ctx.channel
        async for message in channel.history(limit=number, before=ctx.message):
            await message.delete()
        await core.srite_send(ctx, f"Successfully pruned {number} messages")

    @prune.error
    async def prune_handler(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Error handler for prune command"""
        core.debug_info("Running prune handler", error)
        if isinstance(error, commands.MissingRequiredArgument):
            await core.srite_send(
                ctx, "Specify the number of messages to prune. use *prune <num>"
            )
        if isinstance(error, commands.BadArgument):
            await core.srite_send(
                ctx,
                "Specify the number of messages to prune as a number. use *prune <num>",
            )

    @mod.command()
    async def reset(self, ctx: commands.Context, message: discord.Message) -> None:
        """Cleans everything in the channel after the given message (usually by ID)"""
        core.debug_info("Running prune command")
        channel: discord.TextChannel = ctx.channel
        async for message in channel.history(after=message):
            await message.delete()

    @mod.command()
    async def members(self, ctx: commands.Context, guild: discord.Guild = None) -> None:
        """Returns a list of all members in the guild, defaults to current guild"""
        # Default to contextual guild to allow smooth usage
        # TODO: non-default is broken, create custom converter https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#converters
        if not guild:
            guild = ctx.guild
        # Send list of members in codeblock to prevent pinging
        core.debug_info(f"Collecting members of {guild}")
        await core.srite_send(
            ctx, "\n".join(member.mention for member in guild.members)
        )


# Function to add cog
def setup(bot: commands.Bot) -> None:
    """Loads moderal cog"""
    bot.add_cog(Moderation(bot))
