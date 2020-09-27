# friendbot-owm
A weather plugin for checking weather in discord using Open Weather Map.

## Example (in Code)
```
from os import environ
from friendbot.friendbot import Friendbot, FriendbotConfig

owm_api_key = environ["OPEN_WEATHER_MAP_API_KEY"]
config = FriendbotConfig(
    discord_token="thetoken",
    plugin_configs=[
        dict(name="OWMWeather", config=dict(owm_api_key=owm_api_key))
    ]
)
f = Friendbot(config)
f.start()
```

## Example (in Discord)
```
$weather Volcano, Hawaii
@kbougy here is the current forecast for Volcano, Hawaii
Observation Time: 2020-09-27 08:47:23+00
Temperature (F): 70.59
Feels like (F): 73.31
Conditions: :cloud: Broken clouds
Humidity : 83
Wind: 5 mph West Southwest
Sunrise Time: 2020-09-26 16:10:43+00
Sunset Time: 2020-09-27 04:13:17+00
```
