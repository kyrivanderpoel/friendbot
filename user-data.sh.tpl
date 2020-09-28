#!/bin/bash
# Redirect output to somewhere we can look at via AWS console.
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

export OPEN_WEATHER_MAP_API_KEY="${open_weather_map_api_key}"
export DISCORD_BOT_TOKEN="${discord_bot_token}"

sudo yum install git python3 -y
sudo pip3 install virtualenv

cd ~
git clone https://github.com/kbougy/friendbot.git
cd friendbot

virtualenv venv --python=python3
source venv/bin/activate
pip install --editable .

echo 'Starting your best friend!'
friendbot-cli start &