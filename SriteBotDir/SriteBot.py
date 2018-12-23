# HN67's SriteBot
# Invite URL: https://discordapp.com/oauth2/authorize?&client_id=348653600345423873&scope=bot&permissions=0

# Import various modules

# Import core modules for discord API
import discord as discord
from discord.ext import commands
import asyncio

# Import core library modules
import random
import re
import threading
import datetime
import time

import json

import os

# Import config file
import config

# Import core
from core import *

# Import sensitive bot info
import SriteBotInfo

# Set cwd so that bot can be run from anywhere and still functions correctly
os.chdir(os.path.dirname(__file__))


# Initialize bot
bot = commands.Bot(command_prefix=("s.","s:"),
                   description="General bot created by HN67")


# Event that fires once the bot is fully logged in
@bot.event
async def on_ready():
    # Print login information
    debug_info("Bot logged in as",
               bot.user.name,
               bot.user.id)

    # Set activity to help command to give users somewhere to start
    await bot.change_presence(activity=discord.Game(
                              name=(bot.command_prefix[0] + "help")))
    
    # Show that setup is finished (e.g. background tasks have started)
    debug_info("Finished setup")


# Event that fires every message that the bot can see
@bot.event
async def on_message(message):

    # Process commands module commands
    await bot.process_commands(message)


# Ping command
@bot.command()
async def ping(ctx):
    await ctx.send(embed = srite_msg("pong"))
    

# Set the cogs which are to be initally loaded
init_cogs = ["cogs.memes", "cogs.misc",
             "cogs.general", "cogs.timing",
             "cogs.economy"]

# Turn on bot and load extensions, etc
if __name__ == "__main__":

    # Add extensions
    for extension in init_cogs:

        try:
            bot.load_extension(extension)
        except Exception as e:
            debug_info("Failed to load extension {}".format(extension),e)
        else:
            debug_info(f"Loaded extension {extension}")


    # Start bot
    debug_info("Starting bot")
    bot.run(SriteBotInfo.bot_id)
