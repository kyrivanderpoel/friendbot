import attr
from discord.ext import commands

from ...cog import ClassLoggingCog


@attr.s
class Repeater(ClassLoggingCog):
    @commands.command(help="prints whatever text you provide back")
    async def repeat(self, ctx, *args):
        """Returns the args back to the user."""
        await ctx.send(" ".join(args))

