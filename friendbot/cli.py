# TODO: Application logging to cloudwatch logs using Watchtower
import logging
from os import environ

import click

from .friendbot import Friendbot, FriendbotConfig
from .util import suppress_loud_loggers


suppress_loud_loggers()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("/var/tmp/friendbot.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


discord_token = environ["DISCORD_BOT_TOKEN"]
owm_api_key = environ["OPEN_WEATHER_MAP_API_KEY"]

dict_config = dict(
    discord_token=discord_token,
    command_prefix="$",
    plugin_configs=[
        dict(plugin_name="OnReadyLogBotUser"),
        dict(plugin_name="FriendbotInfo"),
        dict(plugin_name="EC2InstanceDetails"),
        dict(plugin_name="Repeater"),
        dict(plugin_name="WordCounter"),
        dict(plugin_name="OWMWeather", config=dict(owm_api_key=owm_api_key)),
        dict(plugin_name="Oncall", config=dict(
            shifts=[
                dict(person="kyri", start_dt="2020-09-28 12:00 PM", end_dt="2020-10-05 12:00 PM"),
                dict(person="kyri", start_dt="2020-11-09 12:00 PM", end_dt="2020-11-16 12:00 PM"),
                dict(person="kyri", start_dt="2020-12-21 12:00 PM", end_dt="2020-12-28 12:00 PM"),
            ]
        )),
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
