import yaml
from flask import (current_app)


def load_yaml():
    """Return the YAML parsed config file."""
    try:
        with open('config/feed_config.yaml', 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
    except yaml.YAMLError as exc:
        current_app.logger.error('YAML read error %s', exc)

    return cfg
