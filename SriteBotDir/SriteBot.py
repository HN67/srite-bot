#HN67's SriteBot
#Invite URL: https://discordapp.com/oauth2/authorize?&client_id=348653600345423873&scope=bot&permissions=0

#Import various modules
import discord
from discord.ext import commands

import os
from pathlib import Path

import random
import re

import json

import SriteBotInfo

#Set cwd so that bot can be run from anywhere and still functions correctly
os.chdir(SriteBotInfo.directory)

#Backup data
'''
with open("SriteBotData.json","r") as file:
    data = json.load(file)

with open("SriteBotDataBackup.json","r") as file:
    backup = json.load(file)

backup[max([int(i) for i in list(backup)])+1] = data

with open("SriteBotDataBackup.json","w") as file:
    json.dump(backup,file)
'''

def debug_info(*messages):
    '''Function for printing seperate information chunks'''
    for line in messages:
        print(line)
    print("-----")

#Initialize bot
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
    #Relable message content
    text = message.content.lower()
    if message.author.id != 348653600345423873:
        '''
        #Change FredBoat nickname based on song queued
        if text.startswith(";;play "):
            #Trim message
            songName = text[7:32]
            #Make sure input is not number, because that is likely selecting
            #from FredBoat options
            if not songName.isdigit():
                #Get FredBoat member object
                fred = message.guild.get_member(184405311681986560)
                #Change FredBoat nick and output confirmation
                await fred.edit(nick="unmute for "+songName)
                await message.channel.send("Changed "+str(fred)+"'s Nickname")
                debug_info("Changed fredboat nick")
        '''
        #Search for certain phrases
        if "im" in text:
            await message.channel.send("hi {0}, im SriteBot".format(text[text.find("im")+2:].strip()))
        elif "http" in text:
            await message.channel.send("lmao tag me")
        elif "lmao" in text:
            await message.channel.send("tag me")
        if "good bot" == text:
            await message.channel.send("thanks hooman")
        #Process commands module commands
    await bot.process_commands(message)
    

@bot.command(short="Greets the bot",description="Gets the bot to reply with Hello,"
             +"and is used to test a variety of things on backend")
async def hello(ctx):
    '''Replies with simple text'''
    await ctx.send("Hi "+ctx.author.nick)
    debug_info("Greeted user",ctx.author.id)

async def rand(ctx, bounds):
    for index in range(len(bounds)-1):
        result = random.randint(bounds[index],bounds[index+1])
        await ctx.send("Random number between " + str(bounds[index]) + " and "
                       + str(bounds[index+1]) + ": "+str(result))

@bot.command(name="rand",description="Generates a random number between numbers provided, inclusive")
async def _rand(ctx, *bounds: int):
    '''Generates a random number'''
    await rand(ctx, bounds)

@bot.command(description="Generates random numbers, the first argument is amount of repetetions")
async def mrand(ctx, *bounds: int):
    '''Generates multiple random numbers'''
    debug_info("Mrand Function activated with  context {0}".format(ctx))
    for i in range(bounds[0]):
        await rand(ctx, bounds[1:])

@_rand.error
async def rand_handler(ctx,error):
    if isinstance(error,discord.ext.commands.BadArgument):
        await ctx.send("Please use whole numbers")
    else:
        print("Unexpected error: ")
        print(error)

@bot.command(description="Returns yes or no")
async def eight(ctx):
    '''Shakes a magic eight ball'''
    if random.randint(1,2) == 2:
        await ctx.send("yes")
    else:
        await ctx.send("no")

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

@meme.command(description="yoda")
async def seagulls(ctx):
    await ctx.send("https://www.youtube.com/watch?v=U9t-slLl30E")

@meme.command(description="sun")
async def angeryr(ctx):
    await ctx.send("https://www.shitpostbot.com/img/sourceimages/angry-doog-angery-57b3a3af935ed.jpeg")

@meme.command(description="glasses")
async def putin(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/185587784218574848/381346915498983435/Funny-Russia-Meme-20.png")

@meme.command(description="james")
async def triger(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/185587784218574848/381347025561714690/trgdd_james.png")

@bot.command(description="o o o")
async def echo(ctx, amount: int, *, message: str):
    for i in range(amount):
        await ctx.send(message)

@echo.error
async def echo_handler(ctx,error):
    if isinstance(error,discord.ext.commands.BadArgument):
        await ctx.send("Please use whole numbers")
    else:
        print("Unexpected error: ")
        print(error)

#RPG of SriteBot
@bot.group(pass_context = True, description = "Header for RPG related commands")
async def rpg(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Specify a rpg command")
        
@rpg.command()
async def setup(ctx):
    debug_info(ctx.author.id,ctx.author.name)
    Path("UserData/{}".format(ctx.author.id)).mkdir(parents=True, exist_ok=True)
    with open("UserData/{}/Info.json".format(ctx.author.id),"w") as file:
        json.dump({"id":ctx.author.id,"name":ctx.author.name},file)
    #with open("UserData/{}/Stats.json".format(ctx.author.id),"w") as file:
        #json.dump({"strength":5,"agility":5,"magic":5,"tech":5,"coin":10},file)
    await ctx.send("You get memed")

bot.run(SriteBotInfo.bot_id)
