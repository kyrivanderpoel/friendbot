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
