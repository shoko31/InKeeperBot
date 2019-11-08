def load_json_data(json_object, key, default_value):
    try:
        return json_object[key]
    except KeyError:
        return default_value

bot_id = [-1]
