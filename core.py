"""SriteBot core functions."""

# Import discord
import discord

# Import config
import config


# Makes sure the guild is equipped to deal with economy (e.g. emoji)
async def sriteEmoji(guild: discord.Guild) -> discord.Emoji:
    """Attempt to obtain a SriteCoin emoji."""
    try:
        for e in guild.emojis:
            if e.name == "sritecoin":
                return e
    # Raised if guild is not a real guild, so does not have .emojis,
    # or somehow an 'emoji' is not a real emoji, has no .name
    except AttributeError:
        # Do nothing, let next block try loading emoji
        pass

    # Did not find sritecoin emoji
    try:
        with open("resources/sritecoin.png", "rb") as i:
            emoji = await guild.create_custom_emoji(name="sritecoin", image=i.read())
        return emoji
    # Forbidden error if bot is not allowed to create a emoji
    # Attribute error if guild is a bad type (e.g. None)
    except (discord.errors.Forbidden, AttributeError):
        return "SC"


# Returns an embed wrapping the text
def srite_msg(value: str) -> discord.Embed:
    """Create a customized embed with the given message."""
    return discord.Embed(color=config.bot.color, description=value)


# Sends an embedded msg to channel
async def srite_send(channel: discord.abc.Messageable, message: str) -> discord.Message:
    """Send the message as an embed."""
    return await channel.send(embed=srite_msg(message))


# Debug method
def debug_info(*messages: object) -> None:
    """Print multiple chunks of information, followed by a spacing line."""
    # Prints each debug in the var-arg
    for line in messages:
        print(line)
    # Prints finishing line
    print("-----")
