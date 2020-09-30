from collections import defaultdict

from tabulate import tabulate
import discord
from discord.ext import commands
import attr

from ...cog import ClassLoggingCog


@attr.s
class OncallShift(object):
    start_dt = attr.ib()
    end_dt = attr.ib()
    person = attr.ib()
    timezone = attr.ib(default="PDT")

    @classmethod
    def list_of_dicts_to_shifts(cls, l):
        return [cls(**d) for d in l]

@attr.s
class OncallConfig(object):
    shifts = attr.ib(converter=OncallShift.list_of_dicts_to_shifts)


@attr.s
class Oncall(ClassLoggingCog):
    @commands.command(help="prints the configured oncall shifts by user")
    async def oncall(self, ctx, *args):
        """Returns the current weather in a nice format"""
        tuple_shifts = [(shift.person, shift.start_dt, shift.end_dt, shift.timezone) for shift in self.config.shifts]
        oncall_table = tabulate(tuple_shifts, headers=["Person", "Shift Start", "Shift End", "TZ"])
        message = f"""
{ctx.author.mention} here are the upcoming oncall shifts:
```
{oncall_table}
```
        """
        await ctx.send(message)
