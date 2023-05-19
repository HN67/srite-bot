"""Roles management cog"""

# Import discord library
import discord
from discord.ext import commands

# Import custom modules
import core
import config
from modules import model


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
        if ctx.guild is None:
            await core.srite_send(ctx, "This command is only available in a server.")
            return
        with model.Guild(guild=ctx.guild).open_roles() as roles_data:
            valid_roles = roles_data["self_roles"]
        # Handles insufficient perms, which means that either the bot doesnt have manage roles perm,
        # or a role higher than the bot was given
        try:
            # Only allows specific roles
            if role in (ctx.guild.get_role(valid) for valid in valid_roles):
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
        if ctx.guild is None:
            await core.srite_send(ctx, "This command is only available in a server.")
            return
        with model.Guild(guild=ctx.guild).open_roles() as roles_data:
            valid_roles = roles_data["self_roles"]
        # Handles insufficient perms, which means that either the bot doesnt have manage roles perm,
        # or a role higher than the bot was given
        try:
            # Only allows specific roles
            if role in (ctx.guild.get_role(valid) for valid in valid_roles):
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

        with model.Guild(guild=ctx.guild).open_roles() as roles_data:
            # Pair roles with enumeration
            for index, role in enumerate(
                ctx.guild.get_role(value) for value in roles_data["self_roles"]
            ):
                # Only try to display the role if it still exists
                if role:
                    embed.add_field(name=index + 1, value=role.name)

        # Send embed
        await ctx.send(embed=embed)

    @roles.command()
    @commands.has_permissions(manage_roles=True)
    async def enable(self, ctx: commands.Context, role: discord.Role) -> None:
        """Enable a role to be a self role."""
        if ctx.guild is None:
            await core.srite_send(ctx, "This command is only available in a server.")
            return
        with model.Guild(guild=ctx.guild).open_roles() as roles_data:
            # Give a message if the role is already a self role
            # This also avoids getting duplicates in the list
            if role.id in roles_data["self_roles"]:
                await core.srite_send(ctx, f"Role {role} is already a self role.")
                return

            roles_data["self_roles"].append(role.id)
            await core.srite_send(ctx, f"Added role {role} to self role list.")

    @roles.command()
    @commands.has_permissions(manage_roles=True)
    async def disable(self, ctx: commands.Context, role: discord.Role) -> None:
        """Disable a role from being a self role."""
        if ctx.guild is None:
            await core.srite_send(ctx, "This command is only available in a server.")
            return
        with model.Guild(guild=ctx.guild).open_roles() as roles_data:
            # Give a descriptive message if the role is not a self role
            if role.id not in roles_data["self_roles"]:
                await core.srite_send(ctx, f"Role {role} is not currently a self role.")
                return

            roles_data["self_roles"].remove(role.id)
            await core.srite_send(ctx, f"Removed role {role} from self role list.")


# Function to add cog
def setup(bot: commands.Bot) -> None:
    """Loads roles cog"""
    bot.add_cog(Roles(bot))
