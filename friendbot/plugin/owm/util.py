condition_to_unicode_emoji = {
    "light rain": ":cloud_with_rain:",
    "broken clouds": ":cloud:",
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
    return condition_to_unicode_emoji.get(condition, "No Emoji :( Bug Kyri to Fix it")


def capitalize_words(s, seperator=" "):
    capital_words = [word.capitalize() for word in s.split(seperator)]
    return seperator.join(capital_words)
