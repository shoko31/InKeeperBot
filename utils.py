from datetime import datetime
from discord.colour import Colour
from discord.embeds import Embed


class Color:

    LIGHT_RED = Colour.from_rgb(252, 92, 101)
    RED = Colour.from_rgb(235, 59, 90)

    LIGHT_BLUE = Colour.from_rgb(69, 170, 242)
    BLUE = Colour.from_rgb(75, 123, 236)
    DARK_BLUE = Colour.from_rgb(56, 103, 214)

    LIGHT_ORANGE = Colour.from_rgb(253, 150, 68)
    ORANGE = Colour.from_rgb(250, 130, 49)

    LIGHT_GREEN = Colour.from_rgb(38, 222, 129)
    GREEN = Colour.from_rgb(32, 191, 107)

    LIGHT_PURPLE = Colour.from_rgb(165, 94, 234)
    PURPLE = Colour.from_rgb(136, 84, 208)

    YELLOW = Colour.from_rgb(254, 211, 48)
    DARK_YELLOW = Colour.from_rgb(247, 183, 49)

    LIGHT_GREY = Colour.from_rgb(209, 216, 224)
    GREY = Colour.from_rgb(165, 177, 194)
    DARK_GREY = Colour.from_rgb(119, 140, 163)


def load_json_data(json_object, key, default_value):
    try:
        return json_object[key]
    except KeyError:
        return default_value


def myconverter(o):
    if isinstance(o, datetime):
        return datetime.strftime(o, '%a %b %d %H:%M:%S %Y')


def simple_embed(title=None, value=None, color=Color.DARK_YELLOW):
    return Embed(title=title, description=value, colour=color)


bot_id = [-1]
COLOR = Color()
