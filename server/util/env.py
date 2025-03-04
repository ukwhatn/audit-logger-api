import os


def get_env(key, default=None):
    return os.environ.get(key, default)


def get_api_keys(env_name: str):
    raw_keys = os.environ.get(env_name, "").split("\n")

    keys = {}

    for key in raw_keys:
        if "|" not in key:
            continue

        app, key = map(str.strip, key.split("|"))
        keys[app] = key

    return keys
