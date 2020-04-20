"""Economy cog"""

# Import python modules
import datetime
import time
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


class Economy(commands.Cog):
    """SriteBot Economy Cog"""

    # Init constructor to reference bot
    def __init__(self, bot: discord.Client):
        self.bot = bot

    # Economy group of SriteBot
    @commands.group(
        pass_context=True,
        description="Header for eco related commands",
        aliases=["eco", "e"],
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
                "{0} has {1} {2}".format(
                    user.display_name,
                    economyData["money"],
                    await core.sriteEmoji(ctx.guild),
                ),
            )

        # Debug info
        core.debug_info(ctx.author.name, ctx.guild, await core.sriteEmoji(ctx.guild))

    @economy.command()
    async def give(
        self, ctx: commands.Context, member: discord.Member, amount: int
    ) -> None:
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
                        embed=core.srite_msg(
                            "{0} sent {2} {3} to {1}".format(
                                ctx.author.display_name,
                                member.display_name,
                                amount,
                                await core.sriteEmoji(ctx.guild),
                            )
                        )
                    )
                else:
                    # Send error message to say there are not enough money
                    await ctx.send(
                        embed=core.srite_msg(
                            "Not enough {}".format(await core.sriteEmoji(ctx.guild))
                        )
                    )

    # Hash command
    @economy.command(aliases=["h"])
    async def hash(self, ctx: commands.Context) -> None:
        """Command to start hash"""

        # Create list of arrows
        arrows = [
            config.uni.leftArrow,
            config.uni.upArrow,
            config.uni.downArrow,
            config.uni.rightArrow,
        ]

        # Create string of numbers for user to reply
        string = []
        for i in range(config.economy.hashLength):
            string.append(random.randint(0, 3))

        # Condense string
        display_string = "".join((arrows[i] for i in string))

        # Display string
        embed = discord.Embed(
            color=config.bot.color, title="Hash", description=display_string
        )
        embed.add_field(name="Last Harvest", value="None")
        display = await ctx.send(embed=embed)

        # Add reactions
        for i in range(4):
            await display.add_reaction(arrows[i])

        # Define the predicate
        def check(reaction: discord.Reaction, user: discord.User) -> bool:
            return reaction.message.id == display.id and user != self.bot.user

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
            embed.set_field_at(
                0,
                name="Last Harvest",
                value=f"{rxn.emoji} by {user.display_name} for 1 {emoji}",
            )

            await display.edit(embed=embed)

            # Give money
            with model.User(user).open_economy() as harvester:
                harvester["money"] += 1

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
            if (diff.days * 86400 + diff.seconds) >= config.economy.taxTime:

                # Add money to user bank
                data["money"] += config.economy.taxAmount

                # Save current time
                data["taxTime"] = current

                # Send confirmation to show sucsess
                await ctx.send(
                    embed=core.srite_msg(
                        "Collected tax of {0} {1}".format(
                            config.economy.taxAmount, await core.sriteEmoji(ctx.guild)
                        )
                    )
                )

            else:
                # Show error message that will tell user how long they need to wait
                cooldown = datetime.timedelta(seconds=config.economy.taxTime)
                rem = cooldown - diff
                # Send message
                await ctx.send(
                    embed=core.srite_msg(f"{rem} remaining before you can tax again")
                )

    # Plant command
    @economy.command(
        aliases=["p"], description="First user to pick the coins keeps them"
    )
    async def plant(self, ctx: commands.Context) -> None:
        """Plants a SriteCoin in the context channel"""

        # Load caller economy data
        with model.User(ctx.author).open_economy() as eco:

            # Check if the caller has a coin to plant
            if not eco["money"] > 0:
                # Show "error" message
                await core.srite_send(
                    ctx, f"You have no {await core.sriteEmoji(ctx.guild)} to plant"
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
            sleep = random.randint(
                config.economy.growTimeMin, config.economy.growTimeMax
            )
            core.debug_info(f"Planting coin from {ctx.author} for {sleep} seconds")
            await asyncio.sleep(sleep)

            # Send growth message
            growth = int(
                (sleep - config.economy.growMatureTime) * config.economy.growRatio
            )
            core.debug_info(f"Sprouted {growth} coins")
            # Edit original plant message
            embed.description += " (Sprouted)"
            await plant.edit(embed=embed)
            # Send notification
            notification = await core.srite_send(
                ctx,
                f"A planted {emoji} has sprouted into {growth} more!\n"
                + "Type `harvest` to harvest them!",
            )
            core.debug_info(f"Sent sprout notification")

            # Wait for harvest message
            message = await self.bot.wait_for(
                "message",
                check=lambda m: m.content == "harvest" and m.channel == ctx.channel,
            )

            # Reply to harvest message
            core.debug_info(f"Harvesting coins for {message.author}")
            await core.srite_send(
                ctx, f"{message.author.display_name} has harvested {growth} {emoji}!"
            )
            # Delete notification message to reduce channel clutter
            await notification.delete()

            # Increase collector money
            with model.User(message.author).open_economy() as eco:
                eco["money"] += growth


# Function to add cog
def setup(bot: commands.Bot) -> None:
    """Loads economy cog"""
    bot.add_cog(Economy(bot))
