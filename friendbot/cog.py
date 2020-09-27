"""Concrete classes using the discord Cog extension.

See: https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
"""
import sys
import inspect
from logging import getLogger

import attr
from discord.ext import commands


@attr.s
class ClassLoggingCog(commands.Cog):
    bot = attr.ib()
    logger = attr.ib(repr=False, init=False)

    @logger.default
    def _get_class_logger(self):
        return getLogger(f"{__name__}.{self.__class__.__name__}")


@attr.s
class OnReadyLogBotUser(ClassLoggingCog):
    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f"Logged in as {self.bot.user}")


@attr.s
class Repeater(ClassLoggingCog):
    @commands.command(help="prints whatever text you provide back")
    async def repeat(self, ctx, *args):
        """Returns the args back to the user."""
        await ctx.send(" ".join(args))


def collect_cogs():
    cls_members = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    blacklist = ["ClassLoggingCog"]
    cog_cls_members = []
    for cls_name, cls in cls_members:
        if cls.__class__.__name__ == "CogMeta" and cls_name not in blacklist:
            cog_cls_members.append(cls)
    return cog_cls_members


# By default we will use all the available cogs.
DEFAULT_COGS = collect_cogs()
