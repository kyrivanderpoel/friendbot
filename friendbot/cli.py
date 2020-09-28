# TODO: Application logging to cloudwatch logs using Watchtower
import logging
from os import environ

import click

from .friendbot import Friendbot, FriendbotConfig
from .util import suppress_loud_loggers


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
suppress_loud_loggers()

discord_token = environ["DISCORD_BOT_TOKEN"]
owm_api_key = environ["OPEN_WEATHER_MAP_API_KEY"]

dict_config = dict(
    discord_token=discord_token,
    command_prefix="$",
    plugin_configs=[
        dict(plugin_name="OnReadyLogBotUser"),
        dict(plugin_name="FriendbotRepo"),
        dict(plugin_name="EC2InstanceDetails"),
        dict(plugin_name="Repeater"),
        dict(plugin_name="OWMWeather", config=dict(owm_api_key=owm_api_key)),
    ]
)

@click.group()
def cli():
    pass

@cli.command()
@click.option("--debug/--no-debug", default=False, help="toggle debug logging")
def start(debug):
    if debug:
        logger.setLevel(logging.DEBUG)
    config = FriendbotConfig.from_dict(dict_config)
    friendbot = Friendbot(config)
    friendbot.start()
