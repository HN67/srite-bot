"""Stocks cog"""

# Import python libraries
import random
import asyncio

# Import discord.py
import discord
from discord.ext import commands

# Import core and config
import core
import config

# Import user data Model
from modules import model


# Function to change stock value
async def update_stocks() -> None:
    """Updates the stocks"""

    with model.Stocks().open() as stocks:
        # Update stocks
        for stock in stocks:
            stocks[stock] += random.randint(
                -1 * config.stocks.change, config.stocks.change
            )


class Stocks(commands.Cog):
    """SriteBot Stocks Cog"""

    # Creates the Cog with a Bot, used when loading the extension
    def __init__(self, bot: discord.Client):
        self.bot = bot

    # Stocks group
    @commands.group(aliases=["s"], description="Buy and sell srite stocks")
    async def stocks(self, ctx: commands.Context) -> None:
        """Stocks command group"""

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
    async def portfolio(
        self, ctx: commands.Context, member: discord.Member = None
    ) -> None:
        """View portfolio of user"""

        # Check member to function on
        if member is None:
            member = ctx.author

        # Create embed
        embed = discord.Embed(
            color=config.bot.color, title=f"{member.display_name} stocks"
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
                        value = amount * stocks[stock]

                        # Add field
                        embed.add_field(
                            name=stock,
                            value="{0} x ({1} {2}) = {3} {2}".format(
                                amount,
                                stocks[stock],
                                await core.sriteEmoji(ctx.guild),
                                value,
                            ),
                        )

                        # Increase total value
                        totalValue += value

                # Add total value field
                embed.add_field(
                    name="Total Value",
                    value="{0} {1}".format(
                        totalValue, await core.sriteEmoji(ctx.guild)
                    ),
                )

        # Send message
        await ctx.send(embed=embed)

    @stocks.command(aliases=["b"])
    async def buy(self, ctx: commands.Context, stock: str, amount: int = 1) -> None:
        """Command to buy stocks"""

        # Open data
        with model.User(ctx.author).open_economy() as eco:
            with model.Stocks().open() as stocks:
                # Check if stock exists (case doesnt matter)
                if stock.upper() in stocks:

                    # Upper stock
                    stock = stock.upper()

                    # Calculate price of purchase (pre increase the price)
                    price = (
                        stocks[stock] + config.stocks.tradeChange * amount
                    ) * amount

                    # Check if user has enough money
                    if eco["money"] >= price:

                        # Decrease money
                        eco["money"] -= price

                        # Increase stocks
                        eco["stocks"][stock] += amount

                        # Change stock price
                        stocks[stock] += config.stocks.tradeChange * amount

                        # Send sucsess message
                        await core.srite_send(
                            ctx,
                            "Bought {0} {1} for {2} {3}".format(
                                amount,
                                stock,
                                price,
                                await core.sriteEmoji(ctx.guild),
                            ),
                        )

                    else:
                        # Send error message
                        await core.srite_send(
                            ctx,
                            "Sorry, you have {0} of {1} {2} {3}".format(
                                eco["money"],
                                price,
                                await core.sriteEmoji(ctx.guild),
                                "required for this purchase",
                            ),
                        )

                else:
                    await core.srite_send(
                        ctx,
                        f"Stock {stock} doesnt exist, use s.s market to view all stocks",
                    )

    @stocks.command(aliases=["s"])
    async def sell(self, ctx: commands.Context, stock: str, amount: int = 1) -> None:
        """Command to sell stocks"""

        # Open data
        with model.User(ctx.author).open_economy() as eco:
            with model.Stocks().open() as stocks:
                # Check if stock exists (case doesnt matter)
                if stock.upper() in stocks:

                    # Upper stock
                    stock = stock.upper()

                    # Calculate price of sale
                    price = stocks[stock] * amount

                    # Check if user has enough stocks
                    if eco["stocks"][stock] >= amount:

                        # Decrease stocks
                        eco["stocks"][stock] -= amount

                        # Increase money
                        eco["money"] += price

                        # Change stock price
                        stocks[stock] -= config.stocks.tradeChange * amount

                        # Send sucsess message
                        await core.srite_send(
                            ctx,
                            "Sold {0} {1} for {2} {3}".format(
                                amount,
                                stock,
                                price,
                                await core.sriteEmoji(ctx.guild),
                            ),
                        )

                    else:
                        # Send error message
                        await core.srite_send(
                            ctx,
                            "Sorry, you have {0} of {1} {2}".format(
                                eco["stocks"][stock],
                                stock,
                                "required for this sale",
                            ),
                        )

                else:
                    await core.srite_send(
                        ctx,
                        f"Stock {stock} doesnt exist, use s.s view to view all stocks",
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


def setup(bot: commands.Bot) -> None:
    """Loads stocks cog"""
    bot.add_cog(Stocks(bot))
