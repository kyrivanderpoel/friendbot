import attr
import discord
from discord.ext import commands

from ...cog import ClassLoggingCog
from .util import tail_logs_to_sprunge


@attr.s
class FriendbotInfo(ClassLoggingCog):
    @commands.command(name="friendbot-repo", help="prints whatever text you provide back")
    async def friendbot_repo(self, ctx, *args):
        """Prints the friendbot repo back to the user."""
        message = f"""
{ctx.author.mention} the friendbot repo is https://github.com/kbougy/friendbot

Feel free to fork of the code and submit a pull request!
        """
        embed = discord.Embed(description=message)
        await ctx.send(embed=embed)

    @commands.command(name="friendbot-logs", help="prints whatever text you provide back")
    async def friendbot_logs(self, ctx, n_lines=10):
        """Prints the last n_lines lines of the log back to the user."""
        message = f"""
{ctx.author.mention} here are the {n_lines} lines of logs you asked for:

{tail_logs_to_sprunge(n_lines)}
        """
        embed = discord.Embed(description=message)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        self.logger.error(f"{event}: {args}, {kwargs}")
        message = """
An unexpected error occurred!

event:  {event}
args:   {args}
kwargs: {kwargs}
        """
        embed = discord.Embed(description=message)
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        self.logger.error(f"Unexpected error occurred: {error}")
        message = f"""
{ctx.author.mention} unexpected error occurred!

{error}
        """
        embed = discord.Embed(description=message)
        await ctx.send(embed=embed)
