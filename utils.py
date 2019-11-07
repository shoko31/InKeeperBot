def load_json_data(json_object, key, default_value):
    try:
        return json_object[key]
    finally:
        return default_value