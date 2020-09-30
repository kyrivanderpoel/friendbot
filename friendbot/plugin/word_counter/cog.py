import re
from collections import Counter

import attr
import discord
from discord.ext import commands
from tabulate import tabulate

from ...cog import ClassLoggingCog

# Any more than this would probably not fit in an embed.
MAX_COUNT = 20

@attr.s
class WordCounter(ClassLoggingCog):
    word_counter = attr.ib(attr.Factory(Counter))

    @commands.command(name="word-counter-most-common-n", help="print the most common words based on stored messages")
    async def word_counter_most_common_n(self, ctx, n=10):
        """Prints the most common n words."""
        count = n if n <= MAX_COUNT else MAX_COUNT
        word_table = tabulate(self.word_counter.most_common(n), headers=["Word", "Count"])
        message = f"""
{ctx.author.mention} the most common {n} words are:

```
{word_table}
```
        """

        embed = discord.Embed(description=message)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.content.startswith("$word-counter-most-common-n"):
            return
        words = [word for word in message.content.split() if word != "$word-counter-most-common-n"]
        self.word_counter += Counter(words)
