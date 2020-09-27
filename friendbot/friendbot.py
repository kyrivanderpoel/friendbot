# TODO: Move the cog_cls logic somwehere else
from logging import getLogger

import attr
from discord.ext import commands
from .plugin.on_ready_log_bot_user.cog import OnReadyLogBotUser
from .plugin.owm.cog import OWMWeather, OWMWeatherConfig
from .plugin.repeater.cog import Repeater

logger = getLogger(__name__)

cog_cls_name_to_cog_cls = {
    "OWMWeather": OWMWeather,
    "OnReadyLogBotUser": OnReadyLogBotUser,
    "Repeater": Repeater,
}

cog_cls_to_config_cls = {
    OWMWeather: OWMWeatherConfig
}


@attr.s(frozen=True)
class FriendbotConfig(object):
    discord_token = attr.ib()
    command_prefix = attr.ib(default="$")
    plugin_configs = attr.ib(default=attr.Factory(list))

    @classmethod
    def from_dict(cls, d):
        return cls(
            discord_token=d["discord_token"],
            command_prefix=d["command_prefix"],
            plugin_configs=d["plugin_configs"],
        )


@attr.s
class Friendbot(object):
    config = attr.ib()
    bot = attr.ib(repr=False, init=False)
    logger = attr.ib(repr=False, init=False)

    def __attrs_post_init__(self):
        self.configure_bot()


    def start(self):
        self.logger.debug(f"Starting bot with token: {self.config.discord_token}")
        self.bot.run(self.config.discord_token)


    def configure_bot(self):
        self.bot = commands.Bot(command_prefix=self.config.command_prefix)
        for plugin_config in self.config.plugin_configs:
            plugin_cls_name = plugin_config["plugin_name"]
            config_dict = plugin_config.get("config")
            cog_cls = cog_cls_name_to_cog_cls[plugin_cls_name]
            plugin_config_cls = cog_cls_to_config_cls.get(cog_cls)

            if plugin_config_cls:
                cog = cog_cls(self.bot, plugin_config_cls(**config_dict))
            else:
                # No config required or available.
                cog =cog_cls(self.bot)

            self.logger.debug(f"Setting up {cog}")
            self.bot.add_cog(cog)

    @logger.default
    def _class_logger(self):
        return getLogger(f"{__name__}.{self.__class__.__name__}")
