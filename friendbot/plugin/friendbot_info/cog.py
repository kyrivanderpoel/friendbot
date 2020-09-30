# TODO: Add support for docker infra
from tabulate import tabulate
import attr
import discord
from discord.ext import commands

from ...cog import ClassLoggingCog
from ...util import bold
from .infrastructure import EC2InstanceInfrastructure, LocalInfrastructure
from .util import tail_logs_to_sprunge, is_running_on_ec2


@attr.s
class FriendbotInfo(ClassLoggingCog):
    _is_running_on_ec2 = attr.ib(default=is_running_on_ec2)


    @commands.command(name="friendbot-repo", help="prints whatever text you provide back")
    async def friendbot_repo(self, ctx, *args):
        """Prints the friendbot repo back to the user."""
        message = f"""
{ctx.author.mention} the friendbot repo is https://github.com/kbougy/friendbot

Feel free to fork of the code and submit a pull request!
        """
        embed = discord.Embed(description=message)
        await ctx.send(embed=embed)

    @commands.command(name="friendbot-infra", help="prints details about the friendbot's host")
    async def friendbot_infra(self, ctx):
        """Returns the args back to the user."""
        data = EC2InstanceInfrastructure() if self._is_running_on_ec2() else LocalInfrastructure()
        self.logger.info(data)
        self.logger.info(data.to_dict())
        table = tabulate(data.to_tuples(), headers=["Detail", "Value"])

        message = f"""
{ctx.author.mention} here are the details about the infrastructure running friendbot:

```
{table}
```
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
