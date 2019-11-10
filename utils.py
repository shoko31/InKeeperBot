from datetime import datetime


def load_json_data(json_object, key, default_value):
    try:
        return json_object[key]
    except KeyError:
        return default_value


def myconverter(o):
    if isinstance(o, datetime):
        return datetime.strftime(o, '%a %b %d %H:%M:%S %Y')

bot_id = [-1]
