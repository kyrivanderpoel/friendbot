from random import choice
import attr
import discord
from discord.ext import commands

from ...cog import ClassLoggingCog
from .hangman import Hangman


@attr.s
class Game(ClassLoggingCog):
    game_state = attr.ib(default=attr.Factory(dict))

    @commands.command(name="game-roll", help="roll")
    async def game_roll(self, ctx, arg1=None, arg2=None):
        """Play a rolling game.

        <number between 1 and 100>
        $game-roll

        <number between 1 and 10>
        $game-roll 10

        <number between 10 and 100>
        $game-roll 10 100
        """
        # No arguments were provided. Use the default range of 1-100
        start = 1
        end = 10
        # Only one argument was provided. Start needs 1 and end needs to be set to arg1
        if arg1 and not arg2:
            start = 1
            end = int(arg1)
        elif arg1 and arg2:
            start = int(arg1)
            end = int(arg2)
        message = f"{ctx.author.mention} is rolling from {start} to {end}... {choice(range(start, end+1))}!"
        await ctx.send(message)


    @commands.command(name="game-hangman", help="play some hangman")
    async def hangman(self, ctx, arg1=None):
        """Play a hangman game."""
        # A guess is required.
        if arg1 is None:
            return await ctx.send(f"{ctx.author.mention} you must provide an guess. Try `$game-hangman a`")

        # Get the existing hangman game or create a new one.
        self.game_state["hangman"] = self.game_state.get("hangman", {})
        if self.game_state["hangman"].get(ctx.author) is None:
            self.game_state["hangman"][ctx.author] = Hangman()
        game = self.game_state["hangman"][ctx.author]

        # Validate that the argument is a valid character, or return a failure.
        choices = game.choices()
        choice_string = ", ".join(choices)
        if not arg1.isalpha():
            return await ctx.send(f"{ctx.author.mention} {arg1} is not a valid character. Pick from {choice_string}.")
        # Validate that the argument is a one length.
        if len(arg1) != 1:
            return await ctx.send(f"{ctx.author.mention} {arg1} must be a single character. Pick from {choice_string}.")
        # We have a single letter. Validate that it hasn't already been selected.
        if game.was_guessed(arg1):
            return await ctx.send(f"{ctx.author.mention} {arg1} was already guessed! pick from. Pick from {choice_string}.")

        # Letter has not been guessed yet. Let's try a guess.
        hit = game.guess(arg1)
        if game.won():
            message = f"""
{ctx.author.mention} {arg1} completed the word! You win!

```
{game.stats_table()}
```
            """
        elif hit:
            message = f"{ctx.author.mention} {arg1} was hit! Current word is {game.hangman_string()}."
        elif game.lost():
            message = f"""
{ctx.author.mention} {arg1} was miss! Gameover!

```
{game.stats_table()}
```
            """
        else:
            message = f"""
{ctx.author.mention} {arg1} was a miss! Current word is {game.hangman_string()}. You have {game.remaining_attempts()} attempts remaining.
            """

        # Persist the game unless it is finished.
        self.game_state["hangman"][ctx.author] = game
        if game.won() or game.lost():
            self.game_state["hangman"][ctx.author] = None
        await ctx.send(embed=discord.Embed(description=message))

