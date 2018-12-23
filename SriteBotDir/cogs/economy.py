# Economy cog
import discord
from discord.ext import commands

# Import modules
import json
import datetime
import time
import random
import asyncio

import os
from pathlib import Path

# Import core and config
from core import *
import config

# Validation of user data function
async def eco_data_validate(member: discord.Member):

    # Check that path exists
    if Path("data/{}".format(member.id)).is_dir():

        pass

    else:

        # Create Path
        Path("data/{}".format(member.id)).mkdir(parents=True, exist_ok=True)

    # Update info file
    with open("data/{}/Info.json".format(member.id), "w") as file:
        json.dump({"id": member.id, "name": member.name}, file)

    # Check state of Economy file
    try:
        with open("data/{}/Economy.json".format(member.id), "r") as file:
            economy = json.load(file)

    # Clause activates if file does not exist
    except FileNotFoundError:
        
        # Create valid economy file since it doesnt exist
        economy = {k: 0 for k in config.economy.attributes}

        # Create stocks tracker
        economy["stocks"] = {k: 0 for k in config.stocks.items}

    # Clause activates if the file exists
    else:
        # Check Economy file data
        # Add any missing keys
        for key in config.economy.attributes:
            if key not in economy:
                economy[key] = 0

        # Validate stock key
        if not "stocks" in economy:
            # Create stocks tracker
            economy["stocks"] = {k: 0 for k in config.stocks.items}
        else:
            # Check each individual key
            for key in config.stocks.items:
                if key not in economy["stocks"]:
                    economy["stocks"][key] = 0

    # Update economy data
    with open("data/{}/Economy.json".format(member.id), "w") as file:
        json.dump(economy, file)

# Validate stock file
async def validate_stocks():
    """Validates the stocks file"""

    stocks = config.stocks.items

    # Make sure stock file exists
    try:

        with open("data/stocks.json", "r") as file:

            # Load it if it does exist
            data = json.load(file)

    except FileNotFoundError:

        # Create stock file
        data = {k: config.stocks.standard for k in stocks}
        debug_info("Created stocks file", data)

    else:

        # Check each stock and create it if it does not exist
        for stock in stocks:
            if stock not in data:
                data[stock] = config.stocks.standard

    # Resave stocks
    with open("data/stocks.json", "w") as file:
        json.dump(data, file)

# Function to change stock value
async def update_stocks():
    """Updates the stocks"""

    # Ensure that all stocks have been initialized
    await validate_stocks()

    # Load stocks
    with open("data/stocks.json", "r") as file:
        stocks = json.load(file)

    # Update stocks
    for stock in stocks:

        stocks[stock] += random.randint(-1 * config.stocks.change,
                                        config.stocks.change)

    # Resave stocks
    with open("data/stocks.json", "w") as file:
        json.dump(stocks, file)        

class Economy:

    # Init constructor to reference bot
    def __init__(self, bot):
        self.bot = bot

    # Economy group of SriteBot
    @commands.group(pass_context=True, description="Header for eco related commands",
               aliases = ["eco","e"])
    async def economy(self, ctx):

        await eco_data_validate(ctx.author)
        
        if ctx.invoked_subcommand is None:
            await ctx.send("Specify a economy command")            

            
    @economy.command(aliases = ["m", "$"])
    async def money(self, ctx, member: discord.Member = None):

        # Choose user to allow varied command use
        if member == None:
            user = ctx.author
        else:
            user = member

        # Save path for cleaner code
        ecoFile = "data/{}/Economy.json".format(user.id)

        # Get data
        with open(ecoFile, "r") as file:
            data = json.load(file)

        # Debug info
        debug_info(ctx.author.name, ctx.guild, await sriteEmoji(ctx.guild))

        # Send message on money amount
        # Create embed
        embed = discord.Embed(color = 0x016681, #00A229
                              description = "{0} has {1} {2}".format(
                                            user.display_name,
                                            data["money"],
                                            await sriteEmoji(ctx.guild)))
        # Send message with embed
        await ctx.send(embed = embed)

            
    @economy.command()
    async def give(self, ctx, member: discord.Member, amount: int):

        # Validate receiver
        await eco_data_validate(member)

        # Pull sender date for later use
        with open("data/{}/Economy.json".format(ctx.author.id)) as file:
            data = json.load(file)

        # Get data of receiver
        with open("data/{}/Economy.json".format(member.id)) as file:
            other = json.load(file)

        # Check if funds are available
        if data["money"] >= amount:

            # Add money to other and remove from self
            other["money"] += amount
            data["money"] -= amount

            # Send confirmation message
            await ctx.send(embed=srite_msg("{0} sent {2} {3} to {1}".format(
                                      ctx.author.display_name,
                                      member.display_name,
                                      amount,
                                      await sriteEmoji(ctx.guild),)
                                     ))

            debug_info(data, other)
            # Resave data
            with open("data/{}/Economy.json".format(ctx.author.id), "w") as file:
                json.dump(data, file)

            with open("data/{}/Economy.json".format(member.id), "w") as file:
                json.dump(other, file)

        else:

            # Send error message to say there are not enough money
            await ctx.send(embed=srite_msg("Not enough {}".format(
                                        await sriteEmoji(ctx.guild))))


    # Hash command
    @economy.command(aliases = ["h"])
    async def hash(self, ctx):

        # Create string of numbers for user to reply
        string = []
        for i in range(1000):
            string.append(random.randint(0, 9))

        # Condense string
        display_string = "".join((str(i) for i in string))

        # Save incremented string
        inc_string = "".join((str(i+1) if i < 9 else "0" for i in string))

        # Display string
        embed = discord.Embed(color = config.bot.color,
                              title = "Hash",
                              description = display_string)
        embed.add_field(name = "Last Harvest", value = "None")
        display = await ctx.send(embed = embed)
        
        # Define the predicate
        def check(msg):
            return (inc_string.startswith(msg.content)
                and msg.channel == ctx.channel and msg.content != "")

        # While the hash still exists
        while len(display_string) > 0:

            debug_info("In hash loop",len(display_string))
            
            # Wait for reply
            msg = await bot.wait_for("message", check = check)

            # Slice off strings
            display_string = display_string[len(msg.content):]
            inc_string = inc_string[len(msg.content):]

            # Update display string
            emoji = await sriteEmoji(msg.guild)
            embed.description = display_string
            embed.set_field_at(0, name = "Last Harvest",
                               value = f"{msg.content} by {msg.author.display_name} for {len(msg.content)} {emoji}")

            await display.edit(embed = embed)
            
            # Validate author
            await eco_data_validate(msg.author)
            
            # Increase collector money
            with open(f"data/{msg.author.id}/Economy.json", "r") as file:
                data = json.load(file)

            data["money"] += len(msg.content)

            with open(f"data/{msg.author.id}/Economy.json", "w") as file:
                json.dump(data, file)

            # Delete messages
            await msg.delete()

        debug_info("Out of hash loop",len(display_string))
    
    # Tax command
    @economy.command()
    async def tax(self, ctx):

        # Save file path to clean code
        ecoFile = "data/{}/Economy.json".format(ctx.author.id)

        # Check last acsessed time to see if it was less than an hour ago
        with open(ecoFile, "r") as file:
            data = json.load(file)

        debug_info(data)
        current = time.time()
        diff = datetime.timedelta(seconds = (current - data["taxTime"]))
        debug_info(current, data["taxTime"], diff, diff.seconds)
        # Check if last tax was an hour ago to determine whether it is to soon
        if (diff.days*86400 + diff.seconds) >= config.economy.taxTime:
            
            # Add money to user bank
            data["money"] += config.economy.taxAmount

            # Save current time
            data["taxTime"] = current
            
            # Resave data
            with open(ecoFile, "w") as file:
                json.dump(data, file)

            # Send confirmation to show sucsess
            await ctx.send(embed = srite_msg("Collected tax of {0} {1}".format(
                            config.economy.taxAmount, await sriteEmoji(ctx.guild))))

        else:
            # Show error message that will tell user how long they need to wait
            cooldown = datetime.timedelta(seconds = config.economy.taxTime)
            rem = cooldown - diff
            # Send message
            await ctx.send(embed = srite_msg(
                            "{} remaining before you can tax again".format(
                            str(rem))))

    ### Stocks area

    # Stocks group
    @commands.group(aliases = ["s"], description = "Buy and sell srite stocks")
    async def stocks(self, ctx):

        # Validate authors economy since stocks are
        # naturally tied to the economy
        await eco_data_validate(ctx.author)

        # Also validate stocks
        await validate_stocks()
        
        if ctx.invoked_subcommand is None:
            await ctx.send("Specify a stock command")


    @stocks.command(aliases = ["m"])
    async def market(self, ctx):
        """View current value of stocks"""

        # Create embed
        embed = discord.Embed(color = config.bot.color, title = "Market")

        # Load stocks
        with open("data/stocks.json", "r") as file:
            stocks = json.load(file)

        # Add fields for each stock
        for stock in stocks:
            embed.add_field(name = stock, value = stocks[stock])

        # Send ebed
        await ctx.send(embed = embed)

    @stocks.command(aliases = ["p", "port", "stocks"])
    async def portfolio(self, ctx, member: discord.Member = None):
        """View portfolio of user"""

        # Check member to function on
        if member is None:
            member = ctx.author

        # Load data
        with open(f"data/{member.id}/Economy.json") as file:
            data = json.load(file)

        # Load stock values
        with open("data/stocks.json") as file:
            stocks = json.load(file)

        # Create embed
        embed = discord.Embed(color = config.bot.color,
                              title = f"{member.display_name} stocks")

        # Init total value var
        totalValue = 0

        # Iterate through all stocks
        for stock, amount in data["stocks"].items():

            # Only show if the user has some of the stock
            if amount > 0:
                # Calculate value
                value = amount*stocks[stock]

                # Add field
                embed.add_field(name = stock,
                                value = "{0} x ({1} {2}) = {3} {2}".format(
                                    amount, stocks[stock],
                                    await sriteEmoji(ctx.guild),
                                    value))

                # Increase total value
                totalValue += value

        # Add total value field
        embed.add_field(name = "Total Value", value = "{0} {1}".format(totalValue,
                                                    await sriteEmoji(ctx.guild)))

        # Send message
        await ctx.send(embed = embed)

    @stocks.command(aliases = ["b"])
    async def buy(self, ctx, stock, amount: int = 1):

        # Load stocks
        with open("data/stocks.json", "r") as file:
            stocks = json.load(file)

        # Load user economy
        with open(f"data/{ctx.author.id}/Economy.json", "r") as file:
            eco = json.load(file)

        # Check if stock exists (case doesnt matter)
        if stock.upper() in stocks:

            # Upper stock
            stock = stock.upper()
            
            # Calculate price of purchase (pre increase the price)
            price = (stocks[stock]+config.stocks.tradeChange*amount)*amount

            # Check if user has enough money
            if eco["money"] >= price:

                # Decrease money
                eco["money"] -= price

                # Increase stocks
                eco["stocks"][stock] += amount

                # Resave data
                with open(f"data/{ctx.author.id}/Economy.json", "w") as file:
                    json.dump(eco, file)

                # Change stock price
                stocks[stock] += config.stocks.tradeChange*amount

                # Save stock data
                with open("data/stocks.json", "w") as file:
                    json.dump(stocks, file)

                # Send sucsess message
                await ctx.send(embed = srite_msg("Bought {0} {1} for {2} {3}".format(
                                                  amount, stock, price,
                                                  await sriteEmoji(ctx.guild))))

            else:
                # Send error message
                await ctx.send(embed = srite_msg("Sorry, you have {0} of {1} {2} {3}".format(
                                eco["money"],
                                price,
                                await sriteEmoji(ctx.guild),
                                "required for this purchase")))

        else:
            await ctx.send(embed = srite_msg(f"Stock {stock} doesnt exist, use s.s view to view all stocks"))


    @stocks.command(aliases = ["s"])
    async def sell(self, ctx, stock, amount: int = 1):

        # Load stocks
        with open("data/stocks.json", "r") as file:
            stocks = json.load(file)

        # Load user economy
        with open(f"data/{ctx.author.id}/Economy.json", "r") as file:
            eco = json.load(file)

        # Check if stock exists (case doesnt matter)
        if stock.upper() in stocks:

            # Upper stock
            stock = stock.upper()
            
            # Calculate price of sale
            price = stocks[stock]*amount

            # Check if user has enough stocks
            if eco["stocks"][stock] >= amount:

                # Decrease stocks
                eco["stocks"][stock] -= amount

                # Increase money
                eco["money"] += price

                # Resave data
                with open(f"data/{ctx.author.id}/Economy.json", "w") as file:
                    json.dump(eco, file)

                # Change stock price
                stocks[stock] -= config.stocks.tradeChange*amount

                # Save stock data
                with open("data/stocks.json", "w") as file:
                    json.dump(stocks, file)

                # Send sucsess message
                await ctx.send(embed = srite_msg("Sold {0} {1} for {2} {3}".format(
                                                  amount, stock, price,
                                                  await sriteEmoji(ctx.guild))))
            else:
                # Send error message
                await ctx.send(embed = srite_msg("Sorry, you have {0} of {1} {2}".format(
                                eco["stocks"][stock],
                                stock,
                                "required for this sale")))

        else:
            await ctx.send(embed = srite_msg(f"Stock {stock} doesnt exist, use s.s view to view all stocks"))


    @stocks.command(hidden = True, aliases = ["u"])
    @commands.is_owner()
    async def update(self, ctx):
        await update_stocks()
        await ctx.send(embed = srite_msg("Updated Stocks"))


    # Extend on_ready to track stocks
    async def on_ready(self):

        debug_info("Economy startup")

        # Track stocks
        self.bot.loop.create_task(self.track_stocks())

        debug_info("Finished economy setup")
        


    # Function designed to be added to the bot as a background task
    async def track_stocks(self):
        """Background task for tracking bot stocks"""

        # Run continuosly during bot operation
        while not self.bot.is_closed():
            # Update stocks every so often
            debug_info("Updating stocks")
            await update_stocks()
            await asyncio.sleep(config.stocks.updateFrequency)


# Function to add cog
def setup(bot):
    bot.add_cog(Economy(bot))
