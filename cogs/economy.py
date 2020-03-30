"""Economy cog"""

# Import python modules
import json
import datetime
import time
import random
import asyncio

from pathlib import Path

# Import discord.py
import discord
from discord.ext import commands

# Import core and config
import core
import config

from modules import model


# Validation of user data function
async def eco_data_validate(member: discord.Member) -> None:
    """Validates and creates a user's economy data if needed"""

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
        if "stocks" not in economy:
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
async def validate_stocks() -> None:
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
        core.debug_info("Created stocks file", data)

    else:

        # Check each stock and create it if it does not exist
        for stock in stocks:
            if stock not in data:
                data[stock] = config.stocks.standard

    # Resave stocks
    with open("data/stocks.json", "w") as file:
        json.dump(data, file)


# Function to change stock value
async def update_stocks() -> None:
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


class Economy(commands.Cog):
    """SriteBot Economy Cog"""

    # Init constructor to reference bot
    def __init__(self, bot: discord.Client):
        self.bot = bot

    # Economy group of SriteBot
    @commands.group(
        pass_context=True,
        description="Header for eco related commands",
        aliases=["eco", "e"]
    )
    async def economy(self, ctx: commands.Context) -> None:
        """Economy command group"""

        if ctx.invoked_subcommand is None:
            await ctx.send("Specify a economy command")

    @economy.command(aliases=["m", "$"])
    async def money(self, ctx: commands.Context, member: discord.Member = None) -> None:
        """Command to show money"""

        # Choose user to allow varied command use
        if member is None:
            user = ctx.author
        else:
            user = member

        # Message the money retrieved by opening the data
        with model.User(user).open_economy() as economyData:
            await core.srite_send(
                ctx,
                f"{user.display_name} has {economyData['money']} {await core.sriteEmoji(ctx.guild)}"
            )

        # Debug info
        core.debug_info(ctx.author.name, ctx.guild, await core.sriteEmoji(ctx.guild))

    @economy.command()
    async def give(self, ctx: commands.Context, member: discord.Member, amount: int) -> None:
        """Command to give other users money"""

        # Open both economy datas
        with model.User(ctx.author).open_economy() as sender:
            with model.User(member).open_economy() as receiver:
                # Check if funds are available
                if sender["money"] >= amount >= 0:
                    # Add money to other and remove from self
                    receiver["money"] += amount
                    sender["money"] -= amount

                    # Send confirmation message
                    await ctx.send(
                        embed=core.srite_msg("{0} sent {2} {3} to {1}".format(
                            ctx.author.display_name,
                            member.display_name,
                            amount,
                            await core.sriteEmoji(ctx.guild),
                        ))
                    )
                else:
                    # Send error message to say there are not enough money
                    await ctx.send(embed=core.srite_msg("Not enough {}".format(
                        await core.sriteEmoji(ctx.guild)
                    )))

    # Hash command
    @economy.command(aliases=["h"])
    async def hash(self, ctx: commands.Context) -> None:
        """Command to start hash"""

        # Create list of arrows
        arrows = [config.uni.leftArrow,
                  config.uni.upArrow,
                  config.uni.downArrow,
                  config.uni.rightArrow]

        # Create string of numbers for user to reply
        string = []
        for i in range(config.economy.hashLength):
            string.append(random.randint(0, 3))

        # Condense string
        display_string = "".join((arrows[i] for i in string))

        # Display string
        embed = discord.Embed(color=config.bot.color,
                              title="Hash",
                              description=display_string)
        embed.add_field(name="Last Harvest", value="None")
        display = await ctx.send(embed=embed)

        # Add reactions
        for i in range(4):
            await display.add_reaction(arrows[i])

        # Define the predicate
        def check(reaction: discord.Reaction, user: discord.User) -> bool:
            return (
                reaction.message.id == display.id
                and user != self.bot.user
            )

        # While the hash still exists
        while len(display_string) > 0:  # pylint: disable=len-as-condition

            core.debug_info("Next char:", display_string[0])

            # Wait for reply
            rxn, user = await self.bot.wait_for("reaction_add", check=check)

            core.debug_info("Valid Event", rxn, user)

            # Delete reaction
            await display.remove_reaction(rxn, user)

            if not rxn.emoji == display_string[0]:
                continue

            # Slice off strings
            display_string = display_string[1:]

            # Update display string
            emoji = await core.sriteEmoji(display.guild)
            embed.description = display_string
            embed.set_field_at(0, name="Last Harvest",
                               value=f"{rxn.emoji} by {user.display_name} for 1 {emoji}")

            await display.edit(embed=embed)

            # Give money
            with model.User(user).open_economy() as harvester:
                harvester["money"] += 1

            # # Validate author
            # await eco_data_validate(user)

            # # Increase collector money
            # with open(f"data/{user.id}/Economy.json", "r") as file:
            #     data = json.load(file)

            # data["money"] += 1

            # with open(f"data/{user.id}/Economy.json", "w") as file:
            #     json.dump(data, file)

        core.debug_info("Out of hash loop", len(display_string))
        await display.delete()

    # Tax command
    @economy.command(aliases=["t"])
    async def tax(self, ctx: commands.Context) -> None:
        """Command to collect periodic tax"""

        # Compare time and previous time
        current = time.time()

        with model.User(ctx.author).open_economy() as data:
            # Calculate time diff
            diff = datetime.timedelta(seconds=(current - data["taxTime"]))
            core.debug_info(current, data["taxTime"], diff, diff.seconds)

            # Check if last tax was an hour ago to determine whether it is to soon
            if (diff.days*86400 + diff.seconds) >= config.economy.taxTime:

                # Add money to user bank
                data["money"] += config.economy.taxAmount

                # Save current time
                data["taxTime"] = current

                # Send confirmation to show sucsess
                await ctx.send(embed=core.srite_msg("Collected tax of {0} {1}".format(
                    config.economy.taxAmount, await core.sriteEmoji(ctx.guild)
                )))

            else:
                # Show error message that will tell user how long they need to wait
                cooldown = datetime.timedelta(seconds=config.economy.taxTime)
                rem = cooldown - diff
                # Send message
                await ctx.send(embed=core.srite_msg(
                    f"{rem} remaining before you can tax again"
                ))

    # Plant command
    @economy.command(
        aliases=["p"],
        description="First user to pick the coins keeps them"
    )
    async def plant(self, ctx: commands.Context) -> None:
        """Plants a SriteCoin in the context channel"""

        # Load caller economy data
        with model.User(ctx.author).open_economy() as eco:

            # Check if the caller has a coin to plant
            if not eco["money"] > 0:
                # Show "error" message
                await core.srite_send(
                    ctx,
                    f"You have no {await core.sriteEmoji(ctx.guild)} to plant"
                )

                planted = False

            else:
                # Save emoji to prevent repeated reloading
                emoji = await core.sriteEmoji(ctx.guild)

                # Show success message
                embed = core.srite_msg(f"Planted a {emoji}")
                plant = await ctx.send(embed=embed)

                # Remove coin
                eco["money"] -= 1

                planted = True

        if planted:

            # Wait random number of seconds within config range
            sleep = random.randint(config.economy.growTimeMin, config.economy.growTimeMax)
            core.debug_info(f"Planting coin from {ctx.author} for {sleep} seconds")
            await asyncio.sleep(sleep)

            # Send growth message
            growth = int((sleep - config.economy.growMatureTime) * config.economy.growRatio)
            core.debug_info(f"Sprouted {growth} coins")
            # Edit original plant message
            embed.description += " (Sprouted)"
            await plant.edit(embed=embed)
            # Send notification
            notification = await core.srite_send(
                ctx,
                f"A planted {emoji} has sprouted into {growth} more!\n" +
                "Type `harvest` to harvest them!"
            )
            core.debug_info(f"Sent sprout notification")

            # Wait for harvest message
            message = await self.bot.wait_for(
                "message",
                check=lambda m: m.content == "harvest" and m.channel == ctx.channel
            )

            # Reply to harvest message
            core.debug_info(f"Harvesting coins for {message.author}")
            await core.srite_send(
                ctx,
                f"{message.author.display_name} has harvested {growth} {emoji}!"
            )
            # Delete notification message to reduce channel clutter
            await notification.delete()

            # Increase collector money
            with model.User(message.author).open_economy() as eco:
                eco["money"] += growth

    # Stocks area
    # Stocks group
    @commands.group(aliases=["s"], description="Buy and sell srite stocks")
    async def stocks(self, ctx: commands.Context) -> None:
        """Stocks command group"""

        # Validate authors economy since stocks are
        # naturally tied to the economy
        await eco_data_validate(ctx.author)

        # Also validate stocks
        await validate_stocks()

        if ctx.invoked_subcommand is None:
            await ctx.send("Specify a stock command")

    @stocks.command(aliases=["m"])
    async def market(self, ctx: commands.Context) -> None:
        """View current value of stocks"""

        # Create embed
        embed = discord.Embed(color=config.bot.color, title="Market")

        # Populate embed
        with model.Stocks().open() as stocks:
            # Add field for each stock
            for stock in stocks:
                embed.add_field(name=stock, value=stocks[stock])

        # Send embed
        await ctx.send(embed=embed)

    @stocks.command(aliases=["p", "port", "stocks"])
    async def portfolio(self, ctx: commands.Context, member: discord.Member = None) -> None:
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
        embed = discord.Embed(
            color=config.bot.color,
            title=f"{member.display_name} stocks"
        )

        # Populate embed
        with model.User(member).open_economy() as data:
            with model.Stocks().open() as stocks:

                # Init total value var
                totalValue = 0

                # Iterate through all stocks
                for stock, amount in data["stocks"].items():

                    # Only show if the user has some of the stock
                    if amount > 0:
                        # Calculate value
                        value = amount*stocks[stock]

                        # Add field
                        embed.add_field(
                            name=stock,
                            value="{0} x ({1} {2}) = {3} {2}".format(
                                amount, stocks[stock],
                                await core.sriteEmoji(ctx.guild),
                                value
                            )
                        )

                        # Increase total value
                        totalValue += value

                # Add total value field
                embed.add_field(
                    name="Total Value",
                    value="{0} {1}".format(
                        totalValue,
                        await core.sriteEmoji(ctx.guild)
                    )
                )

        # Send message
        await ctx.send(embed=embed)

    @stocks.command(aliases=["b"])
    async def buy(self, ctx: commands.Context, stock: str, amount: int = 1) -> None:
        """Command to buy stocks"""

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
                await ctx.send(embed=core.srite_msg("Bought {0} {1} for {2} {3}".format(
                    amount, stock, price, await core.sriteEmoji(ctx.guild)
                )))

            else:
                # Send error message
                await ctx.send(embed=core.srite_msg("Sorry, you have {0} of {1} {2} {3}".format(
                    eco["money"], price,
                    await core.sriteEmoji(ctx.guild), "required for this purchase"
                )))

        else:
            await ctx.send(
                embed=core.srite_msg(f"Stock {stock} doesnt exist, use s.s view to view all stocks")
            )

    @stocks.command(aliases=["s"])
    async def sell(self, ctx: commands.Context, stock: str, amount: int = 1) -> None:
        """Command to sell stocks"""

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
                await ctx.send(embed=core.srite_msg("Sold {0} {1} for {2} {3}".format(
                    amount, stock, price, await core.sriteEmoji(ctx.guild)
                )))

            else:
                # Send error message
                await ctx.send(embed=core.srite_msg("Sorry, you have {0} of {1} {2}".format(
                    eco["stocks"][stock], stock, "required for this sale"
                )))

        else:
            await ctx.send(
                embed=core.srite_msg(f"Stock {stock} doesnt exist, use s.s view to view all stocks")
            )

    @stocks.command(hidden=True, aliases=["u"])
    @commands.is_owner()
    async def update(self, ctx: commands.Context) -> None:
        """Command to update the stock market"""
        await update_stocks()
        await ctx.send(embed=core.srite_msg("Updated Stocks"))

    # Extend on_ready to track stocks
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Bot on ready listener"""

        core.debug_info("Economy startup")

        # Track stocks
        self.bot.loop.create_task(self.track_stocks())

        core.debug_info("Finished economy setup")

    # Function designed to be added to the bot as a background task
    async def track_stocks(self) -> None:
        """Background task for tracking bot stocks"""

        # Run continuosly during bot operation
        while not self.bot.is_closed():
            # Update stocks every so often
            core.debug_info("Updating stocks")
            await update_stocks()
            await asyncio.sleep(config.stocks.updateFrequency)


# Function to add cog
def setup(bot: commands.Bot) -> None:
    """Loads economy cog"""
    bot.add_cog(Economy(bot))
