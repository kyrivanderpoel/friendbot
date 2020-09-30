"""This module implements functions that collect plugins and their configurations.

# TODO: Discover a way to load all of these plugins without declaring them at the top of the file
"""
import inspect
import sys

from .friendbot_info.cog import FriendbotInfo
from .on_ready_log_bot_user.cog import OnReadyLogBotUser
from .owm.cog import OWMWeather, OWMWeatherConfig
from .oncall.cog import Oncall, OncallConfig
from .repeater.cog import Repeater
from .word_counter.cog import WordCounter
from .game.cog import Game


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
