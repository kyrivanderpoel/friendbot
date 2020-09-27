import attr
from discord.ext import commands

from ...cog import ClassLoggingCog


@attr.s
class OnReadyLogBotUser(ClassLoggingCog):
    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f"Logged in as {self.bot.user}")
