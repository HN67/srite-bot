# SriteBot core functions file
# Import discord
import discord
from discord.ext import commands

# Import config
import config

# Makes sure the guild is equipped to deal with economy (e.g. emoji)
async def sriteEmoji(guild: discord.Guild):

    for e in guild.emojis:
        if e.name == "sritecoin":
            return e

    else:
        try:
            with open("resources/sritecoin.png", "rb") as i:
                emoji = await guild.create_custom_emoji(name="sritecoin",
                                                        image = i.read())
            return emoji
        except discord.errors.Forbidden: 
            return "SC (No emoji perms)"

# Returns an embed wrapping the text
def srite_msg(value: str):

    return discord.Embed(color = config.bot.color, description = value)

# Sends an embedded msg to channel
async def srite_send(channel: discord.TextChannel, message: str):

    await channel.send(embed = srite_msg(message))

# Debug method
def debug_info(*messages):
    '''Function for printing seperate information chunks'''
    # Prints each debug in the var-arg
    for line in messages:
        print(line)
    # Prints finishing line
    print("-----")
