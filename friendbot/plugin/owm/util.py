# TODO: Keep using the command to add more emojis
condition_to_unicode_emoji = {
    "light rain": ":cloud_with_rain:",
    "broken clouds": ":white_sun_small_cloud:",
    "scattered clouds": ":white_sun_small_cloud:",
    "clear sky": ":sunny:",
    "fog": ":fog:",
}


def angle_to_direction(angle):
    val = int((angle / 22.5) + .5)
    lst = [
        "North",
        "North Northeast",
        "Northeast",
        "East Northeast",
        "East",
        "East Southeast",
        "South East",
        "South Southeast",
        "South",
        "South Southwest",
        "South West",
        "West Southwest",
        "West",
        "West Northwest",
        "North West",
        "North Northwest",
    ]
    return lst[(val % 16)]


def get_emoji(condition):
    condition = condition.lower()
    return condition_to_unicode_emoji.get(condition, "")


def capitalize_words(s, seperator=" "):
    capital_words = [word.capitalize() for word in s.split(seperator)]
    return seperator.join(capital_words)
