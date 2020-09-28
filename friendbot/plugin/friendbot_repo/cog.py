import attr
import discord
from discord.ext import commands

from ...cog import ClassLoggingCog


@attr.s
class FriendbotRepo(ClassLoggingCog):
    @commands.command(name="friendbot-repo", help="prints whatever text you provide back")
    async def friendbot_repo(self, ctx, *args):
        """Prints the friendbot repo back to the user."""
        message = f"""
{ctx.author.mention} the friendbot repo is https://github.com/kbougy/friendbot

Feel free to fork of the code and submit a pull request!
        """
        embed = discord.Embed(description=message)
        await ctx.send(embed=embed)
