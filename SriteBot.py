"""
HN67's SriteBot
https://discordapp.com/oauth2/authorize?&client_id=348653600345423873&scope=bot&permissions=0
"""

# Import python modules
from typing import Callable, Any
import os

# Import core modules for discord API
import discord
from discord.ext import commands

# Import config file
import config

# Import core
import core

# Import sensitive bot info
import SriteBotInfo

# Set cwd so that bot can be run from anywhere and still functions correctly
os.chdir(os.path.dirname(__file__))


# Initialize bot
bot = commands.Bot(
    command_prefix=config.bot.prefixes, description="General bot created by HN67"
)


# Event that fires once the bot is fully logged in
@bot.event
async def on_ready() -> None:
    """Callback run once bot is fully logged in"""

    # Print login information
    core.debug_info("Bot logged in as", bot.user.name, bot.user.id)

    # Set activity to help command to give users somewhere to start
    await bot.change_presence(
        activity=discord.Game(name=(bot.command_prefix[0] + "help"))
    )

    # Show that setup is finished (e.g. background tasks have started)
    core.debug_info("Finished setup")


# Event that fires every message that the bot can see
@bot.event
async def on_message(message: discord.Message) -> None:
    """Callback run whenever a messege is sent"""

    # Process commands module commands
    await bot.process_commands(message)


# Save default handler since it gets overriden by the event
default_error_handler = bot.on_command_error


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
    """Callback run when there is an error running a command"""

    # Only run global handler if command-local is not provided
    # hasattr technique taken from discord.py default on_command_error source
    if not hasattr(ctx.command, "on_error"):

        # Notify user so that the bot doesn't silently fail
        await core.srite_send(ctx, f"Oops, something went wrong.\n```{error}```")

        # Call default handling to preserve std.err output
        await default_error_handler(ctx, error)


# Ping command
@bot.command()
async def ping(ctx: commands.Context) -> None:
    """Ping command to test bot connectivity"""
    await ctx.send(embed=core.srite_msg("pong"))


# Test command for various things
@bot.command()
async def test(ctx: commands.Context, number: int) -> None:
    """Test command to test various features"""
    await core.srite_send(ctx.channel, str(number + 1))


@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx: commands.Context) -> None:
    """Reloads all extensions"""
    # Reload extensions
    core.debug_info("Reloading extensions")
    success = handle_extensions(bot.reload_extension)

    # Send confirmation message
    if success:
        await core.srite_send(ctx, "Reloaded extensions")
    else:
        await core.srite_send(ctx, "At least one extension failed to reload")


# Set the cogs which are to be initally loaded
extensions = [
    "cogs.memes",
    "cogs.misc",
    "cogs.general",
    "cogs.timing",
    "cogs.economy",
    "cogs.stocks",
    "cogs.moderation",
    "cogs.roles",
]


def handle_extensions(handler: Callable[[str], Any]) -> bool:
    """Calls the given method on each of the extension strings. Intended to load/etc
    Returns False if an exception is thrown when loading any extension, True if none thrown
    """
    success = True
    for extension in extensions:
        try:
            handler(extension)
        except Exception as e:  # pylint: disable=broad-except
            core.debug_info(
                f"Failed to use {handler.__name__} on extension {extension}", e
            )
            success = False
        else:
            core.debug_info(f"Used {handler.__name__} on extension {extension}")
    return success


# Turn on bot and load extensions, etc
if __name__ == "__main__":

    # Add extensions
    handle_extensions(bot.load_extension)

    # Start bot
    core.debug_info("Starting bot")
    bot.run(SriteBotInfo.bot_id)
