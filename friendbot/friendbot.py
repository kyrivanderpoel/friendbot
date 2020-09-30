# TODO: Move the cog_cls logic somwehere else
import inspect
import sys
from logging import getLogger


import attr
from discord.ext import commands

from .plugin.ec2_instance_details.cog import EC2InstanceDetails
from .plugin.friendbot_info.cog import FriendbotInfo
from .plugin.on_ready_log_bot_user.cog import OnReadyLogBotUser
from .plugin.owm.cog import OWMWeather, OWMWeatherConfig
from .plugin.oncall.cog import Oncall, OncallConfig
from .plugin.repeater.cog import Repeater
from .plugin.word_counter.cog import WordCounter

logger = getLogger(__name__)

def generate_cog_cls_name_to_cog_cls():
    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    return {cls_name: cls for cls_name, cls in clsmembers if cls.__class__.__name__ == "CogMeta"}

cog_cls_name_to_cog_cls = generate_cog_cls_name_to_cog_cls()

def generate_cog_cls_to_config_cls():
    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    # Get all the cog classes
    cog_cls_to_config_cls = {v: None for _k, v in cog_cls_name_to_cog_cls.items()}
    for cls_name, cls in clsmembers:
        if cls_name.endswith("Config") and cls_name.rstrip("Config") in cog_cls_name_to_cog_cls:
            cog_cls = cog_cls_name_to_cog_cls[cls_name.rstrip("Config")]
            cog_cls_to_config_cls[cog_cls] = cls

    return {k: v for k, v in cog_cls_to_config_cls.items() if v is not None}

cog_cls_to_config_cls = generate_cog_cls_to_config_cls()


@attr.s(frozen=True)
class FriendbotConfig(object):
    discord_token = attr.ib(repr=lambda x: "redacted")
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
