from logging import getLogger

import attr
from discord.ext import commands
from .cog import DEFAULT_COGS

logger = getLogger(__name__)


@attr.s
class Friendbot(object):
    discord_token = attr.ib()
    command_prefix = attr.ib(default="$")
    cog_classes = attr.ib(default=DEFAULT_COGS)
    logger = attr.ib(repr=False, init=False)


    def start(self):
        bot = commands.Bot(command_prefix=self.command_prefix)
        for cog_class in self.cog_classes:
            cog = cog_class(bot)
            self.logger.debug(f"Setting up {cog}")
            bot.add_cog(cog)
        self.logger.debug(f"Starting bot with token: {self.discord_token}")
        bot.run(self.discord_token)

    @logger.default
    def _class_logger(self):
        return getLogger(f"{__name__}.{self.__class__.__name__}")
