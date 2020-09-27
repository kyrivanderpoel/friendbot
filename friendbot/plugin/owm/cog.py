# TODO: Handle bad weather
# TODO: Move generating the weather message outside of the weather command
import datetime

import discord
from discord.ext import commands
from pyowm import OWM
import attr

from ...cog import ClassLoggingCog
from .util import angle_to_direction, get_emoji, capitalize_words


@attr.s
class OWMWeatherConfig(object):
    owm_api_key = attr.ib(repr=lambda x: "redacted")


@attr.s
class OWMWeather(ClassLoggingCog):
    owm = attr.ib()

    @owm.default
    def _get_owm(self):
        return OWM(self.config.owm_api_key)


    @commands.command(help="print the current weather conditions")
    async def weather(self, ctx, *args):
        """Returns the current weather in a nice format"""
        # Search for current weather in London (Great Britain)
        weather_manager = self.owm.weather_manager()
        place = " ".join(args)
        observation = weather_manager.weather_at_place(place)


        weather = observation.weather
        temperature = observation.weather.temperature("fahrenheit")
        detailed_status = capitalize_words(weather.detailed_status)
        wind = weather.wind(unit='miles_hour')
        weather_message = f"""
{ctx.author.mention} here is the current forecast for {place}
Observation Time: {weather.reference_time(timeformat="iso")}
Temperature (F): {temperature["temp"]}
Feels like (F): {temperature["feels_like"]}
Conditions: {get_emoji(detailed_status)} {detailed_status}
Humidity : {weather.humidity}
Wind: {round(wind["speed"])} mph {angle_to_direction(wind["deg"])}
Sunrise Time: {weather.sunrise_time(timeformat="iso")}
Sunset Time: {weather.sunset_time(timeformat="iso")}
        """
        embed = discord.Embed(description=weather_message)
        await ctx.send(embed=embed)
