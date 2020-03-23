# General commands cog for SriteBot
import discord
from discord.ext import commands

# Import core libraries
import random
import json

import core

# Cog class
class General(commands.Cog):

    # Init to reference bot
    def __init__(self, bot):
        self.bot = bot

    # Greeting command    
    @commands.command(short="Greets the bot", description="Gets the bot to reply with Hello,"
                                                     + "and is used to test a variety of things on backend")
    async def hello(self, ctx):
        '''Replies with simple text'''
        try:
            await ctx.send("Hi " + ctx.author.nick)
        except TypeError:
            await ctx.send("Hi " + ctx.author.name)
        core.debug_info("Greeted user", ctx.author.id)

    # Eightball command
    @commands.command(description="Returns yes or no")
    async def eight(self, ctx):
        '''Shakes a magic eight ball'''
        # Store options for response in tuple
        options = ("yes","no","absolutely","maybe","hardly","sure","never")
        # Respond with random option using .choice
        await ctx.send(random.choice(options))

    @commands.command(description="o o o")
    async def echo(self, ctx, amount: int, *, message: str):
        """o o o"""
        for i in range(amount):
            await ctx.send(message)

    # Echo command
    @echo.error
    async def echo_handler(self, ctx, error):
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send("Please use whole numbers")
        else:
            print("Unexpected error: ")
            print(error)

    # Open console command
    @commands.command(hidden = True)
    @commands.is_owner()
    async def console(self, ctx):
        """Opens the console to input, only available to HN67"""
        await ctx.message.delete()
        temp = input("Request for console input: ")
        await ctx.send(temp)

    @commands.command()
    async def dabs(self, ctx):
        """Check your total dabs"""
        with open("data/count.json", "r") as file:
            count = json.load(file)
        core.debug_info(count,ctx.author.name)
        if ctx.author.name in count["dab"]:
            await ctx.send(f"Total {ctx.author.name} Dabs: {count['dab'][ctx.author.name]}")
        else:
            await ctx.send("Congratulations, you have never dabbed")


    # On message event
    async def on_message(self, message):
        
        # Make sure author is not SriteBot (prevent loops)
        if message.author.id != 348653600345423873:

            # Relable message content
            text = message.content.lower()
            # Relable channel
            channel = message.channel
            # Relable author
            author = message.author
            
            # Search for certain phrases
            if "im " in text:
                await channel.send("hi {0}, im SriteBot.".format(
                                    text[text.find("im") + 2:].strip()))

            elif "http" in text:
                if random.randint(1,2) == 1:
                    await channel.send("[removed]")
                    
            elif "lmao" in text:
                await channel.send("tag me")
                
            if "good bot" == text:
                await channel.send("thanks human")
                
            elif "hello" == text:
                await channel.send("owo whats this")
                
            if "dab" in text:
                await count_dabs(message)
            
        
# Function to parse message for dabs
async def count_dabs(message):

    # Relable message content
    text = message.content.lower()
    # Relable channel
    channel = message.channel
    # Relable author
    author = message.author
    
    # Load count file
    with open("data/dabs.json", "r") as file:
        count = json.load(file)
        
    # Save original
    try:
        original = count["total"]
    except KeyError:
        original = 0
        
    # Increment/Create dab counter
    core.debug_info(count)
    
    # Total counter
    try:
        count["total"] += text.count("dab")
    except KeyError:
        count["total"] = text.count("dab")

    # Individual counter    
    try:
        count[author.name] += text.count("dab")
    except KeyError:
        count[author.name] = text.count("dab")
        
    # Redump json file
    with open("data/dabs.json", "w") as file:
        json.dump(count, file)
        
    # Display count
    await channel.send("```Dab Count: {0}\nLast Dab: {1}```"
                 .format(count["total"],message.author))

    # Track 1000 milestones
    if (original//1000) != (count["total"]//1000):
        await channel.send("Jesus, {} Dabs!".format(count["total"]//1000*1000))


# Setup function to load cog
def setup(bot):
    bot.add_cog(General(bot))
