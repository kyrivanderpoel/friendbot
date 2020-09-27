# friendbot

A bot for Discord written in Python.

## Install
```
$ pip install --editable .
```

## Usage


```
export DISCORD_BOT_TOKEN=thetoken
friendbot-cli start --debug
```

You'll see something like this:
```
$ friendbot-cli start --debug
2020-09-26 22:17:50,457 - discord.client - WARNING - PyNaCl is not installed, voice will NOT be supported
2020-09-26 22:17:50,457 - friendbot.friendbot.Friendbot - DEBUG - Setting up OnReadyLogBotUser(bot=<discord.ext.commands.bot.Bot object at 0x1019eff40>)
2020-09-26 22:17:50,458 - friendbot.friendbot.Friendbot - DEBUG - Setting up Repeater(bot=<discord.ext.commands.bot.Bot object at 0x1019eff40>)
2020-09-26 22:17:50,458 - friendbot.friendbot.Friendbot - DEBUG - Starting bot with token: redacted
2020-09-26 22:17:53,016 - friendbot.cog.OnReadyLogBotUser - INFO - Logged in as somecooluser#0000
```

In discord:
```
$help
$help <command>
```
