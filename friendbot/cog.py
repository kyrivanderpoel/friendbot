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
    config = attr.ib(default=None)
    logger = attr.ib(repr=False, init=False)

    @logger.default
    def _get_class_logger(self):
        return getLogger(f"{__name__}.{self.__class__.__name__}")
