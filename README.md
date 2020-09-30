# friendbot

A bot for Discord written in Python.

## Install
```
$ pip install --editable .
```

## Usage


```
export DISCORD_BOT_TOKEN=thetoken
export OPEN_WEATHER_MAP_API_KEY=thekey
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

## Run Locally
Create a .env file with the environment variables listed under environment in the docker-compose.yml.
```
docker-compose build && docker-compose up
```

## Deploy
Create a secrets file (e.g. secrets.tfvars)

```
discord_bot_token=thetoken
open_weather_map_api_key=thekey
```

Setup the terraform resources
```
terraform init
terraform plan -var-file="secrets.tfvars"
```

Create the EC2 instance and start up friendbot as a background process.
As of now you can only get the logs via Console Logs: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-console.html#instance-console-console-output

```
terraform apply -var-file="secrets.tfvars"
```

Destroy the resources
```
terraform destory -var-file="secrest.tfvars"
```

## Todo
- Implement actual config file to get my oncall schedule out of the default configuration
- Setup logging to cloudwatch
- Plugin that prints application logs from cloudwatch to discord
- Reduce duplication of vars in .env and secrets.tfvars. There has to be a way to only need one of those...


