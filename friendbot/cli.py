import logging
from os import environ

import click

from .friendbot import Friendbot
from .util import suppress_loud_loggers


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
suppress_loud_loggers()


@click.group()
def cli():
    pass

@cli.command()
@click.option("--debug/--no-debug", default=False, help="toggle debug logging")
def start(debug):
    if debug:
        logger.setLevel(logging.DEBUG)
    discord_token = environ["DISCORD_BOT_TOKEN"]
    friendbot = Friendbot(discord_token=discord_token)
    friendbot.start()
