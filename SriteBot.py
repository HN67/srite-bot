import discord
from discord.ext import commands

import os

import random
import re

os.chdir("C:\\Users\\Allard Family\\Desktop\\Stuff\\PythonFiles")

def debug_info(*messages):
    for line in messages:
        print(line)
    print("-----")

bot = commands.Bot(command_prefix = "s:",description = "General bot created by HN67")

@bot.event
async def on_ready():
    debug_info("Bot logged in as",
               bot.user.name,
               bot.user.id)
    await bot.change_presence(game=discord.Game(name=(bot.command_prefix+"help")))
    debug_info("Finished setup")

@bot.event
async def on_message(message):
    if message.content.startswith(";;play "):
        songName = message.content[7:32]
        if not songName.isdigit():
            fred = message.guild.get_member(184405311681986560)
            await fred.edit(nick="unmute for "+songName)
            await message.channel.send("Changed "+str(fred)+"'s Nickname")
            debug_info("Changed fredboat nick")
    await bot.process_commands(message)

@bot.command(short="Greets the bot",description="Gets the bot to reply with Hello,"
             +"and is used to test a variety of things on backend")
async def hello(ctx):
    await ctx.send("Hi "+ctx.author.nick)
    debug_info("Greeted user")

@bot.command(description="Generates a random number between numbers provided, inclusive")
async def rand(ctx, *bounds: int):
    for index in range(len(bounds)-1):
        result = random.randint(bounds[index],bounds[index+1])
        await ctx.send("Random number between " + str(bounds[index]) + " and "
                       + str(bounds[index+1]) + ": "+str(result))

@rand.error
async def rand_handler(ctx,error):
    if isinstance(error,discord.ext.commands.BadArgument):
        await ctx.send("Please use whole numbers")
    else:
        print("Unexpected error: ")
        print(error)

@bot.group(pass_context = True,description="follow with a specific meme")
async def meme(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Specify a meme")

@meme.command(description="dot dab")
async def dab(ctx):
    await ctx.send(file=discord.File("dab.jpg"))

@meme.command(description="doge")
async def angery(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/32440271559"+
                  "5767809/353676898892775424/angerydoge.jpg")

@meme.command(description="laser")
async def notyet(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/32440271559"+
                  "5767809/353676953800278016/NotYet.png")

bot.run("MzQ4NjUzNjAwMzQ1NDIzODcz.DI-qRw.gXyJhyVZuPzTroN5B9TcsIQa_ik")
