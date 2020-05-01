"""Roles management cog"""

# Import discord library
import discord
from discord.ext import commands

# Import custom modules
import core
import config


class Roles(commands.Cog):
    """SriteBot roles management cog"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def roles(self, ctx: commands.Context) -> None:
        """Command group for role management"""
        await core.srite_send(ctx, "Specify a subcommand, such as `add` or `remove`")

    @roles.command()
    async def add(self, ctx: commands.Context, role: discord.Role) -> None:
        """Adds a role to the author"""
        core.debug_info("Adding role", role, type(role))
        # Handles insufficient perms, which means that either the bot doesnt have manage roles perm,
        # or a role higher than the bot was given
        try:
            # Only allows specific roles
            if role in (
                ctx.guild.get_role(valid) for valid in config.roles.valid_roles
            ):
                await ctx.author.add_roles(role)
                await core.srite_send(
                    ctx, f"Role {role} added to {ctx.author.display_name}"
                )
            else:
                await core.srite_send(
                    ctx, "Sorry, that role is not permitted to be added by the bot."
                )
        except discord.Forbidden:
            await core.srite_send(
                ctx,
                "Sorry, the bot doesn't have sufficient permissions to add this role",
            )

    async def role_change_handler(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Common error handler for manipulating roles"""
        # Invalid role
        if isinstance(error, commands.BadArgument):
            await core.srite_send(ctx, "Couldn't find specified role")
        # No role/argument given
        elif isinstance(error, commands.MissingRequiredArgument):
            await core.srite_send(ctx, "Missing required role argument")
        elif isinstance(error, commands.UserInputError):
            await core.srite_send(ctx, "An error occured with user input")
        else:
            await core.srite_send(
                ctx, "An unexpected error occured; please contact the bot owner"
            )
            core.debug_info("Unhandled exception", type(error), error)

    @add.error
    async def add_handler(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Error handler for add command"""
        await self.role_change_handler(ctx, error)

    @roles.command()
    async def remove(self, ctx: commands.Context, role: discord.Role) -> None:
        """Removes a role from the author"""
        core.debug_info("Removing role", role, type(role))
        # Handles insufficient perms, which means that either the bot doesnt have manage roles perm,
        # or a role higher than the bot was given
        try:
            # Only allows specific roles
            if role in (
                ctx.guild.get_role(valid) for valid in config.roles.valid_roles
            ):
                await ctx.author.remove_roles(role)
                await core.srite_send(
                    ctx, f"Role {role} removed from {ctx.author.display_name}"
                )
            else:
                await core.srite_send(
                    ctx, "Sorry, that role is not permitted to be removed by the bot."
                )
        except discord.Forbidden:
            await core.srite_send(
                ctx,
                "Sorry, the bot doesn't have sufficient permissions to remove this role",
            )

    @remove.error
    async def remove_handler(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Error handler for remove command"""
        await self.role_change_handler(ctx, error)

    @roles.command()
    async def available(self, ctx: commands.Context) -> None:
        """Displays the roles available for individual manipulation"""
        # Create embed
        embed = discord.Embed(color=config.bot.color, title="Available Roles")

        # Pair roles with enumeration
        for index, role in enumerate(
            ctx.guild.get_role(value) for value in config.roles.valid_roles
        ):
            embed.add_field(name=index + 1, value=role.name)

        # Send embed
        await ctx.send(embed=embed)


# Function to add cog
def setup(bot: commands.Bot) -> None:
    """Loads roles cog"""
    bot.add_cog(Roles(bot))
