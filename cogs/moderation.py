"""Moderation tools cog"""

import time
import typing as t

# Import discord
import discord
from discord.ext import commands

# Import core
import core
from modules import model


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
    async def members(
        self, ctx: commands.Context, guildID: t.Optional[int] = None
    ) -> None:
        """Returns a list of all members in the guild (by id), defaults to current guild"""
        # Default to contextual guild to allow smooth usage
        # If number is given, retrieve the guild from bot
        # Will fail if the bot is not in the given server.
        # We do this instead of a annotation because apparently
        # Guild doesnt work for annotation converter
        guild: discord.Guild
        if not guildID:
            guild = ctx.guild
        else:
            guild = ctx.bot.get_guild(guildID)
        # Send list of members in codeblock to prevent pinging
        core.debug_info(f"Collecting members of {guild}")
        await core.srite_send(
            ctx, "\n".join(member.mention for member in guild.members)
        )

    @mod.command()
    async def clean(self, ctx: commands.Context, before: discord.Message) -> None:
        """Clean old messages from a channel.

        Archives and removes all messages before the specified message.
        """
        core.debug_info("Running clean command")

        limit = 1000
        await core.srite_send(
            ctx, f"Collecting oldest {limit} messages before {before.id}."
        )

        messages: t.List[discord.Message] = [
            message
            async for message in ctx.channel.history(
                limit=1000, before=before, oldest_first=True
            )
        ]

        message_data = [
            {
                "guild": message.guild.id,
                "channel": message.channel.id,
                "id": message.id,
                "author": message.author.id,
                "author_name": message.author.name,
                "content": message.content,
                "time": str(message.created_at),
            }
            for message in messages
        ]

        # core.debug_info(*messages)

        model.archive(name=str(int(time.time())), data=message_data)
        await core.srite_send(ctx, "Archived messages.")

        await core.srite_send(ctx, "Deleting messages.")
        for message in messages:
            await message.delete()

        await core.srite_send(ctx, "Messages cleaned.")


# Function to add cog
def setup(bot: commands.Bot) -> None:
    """Loads moderal cog"""
    bot.add_cog(Moderation(bot))
