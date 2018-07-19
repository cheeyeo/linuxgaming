"""
helper module with various functions

"""

import json
import yaml
import feedparser
import requests
from flask import (current_app, abort)


def load_yaml():
    """
    parse the configuration file

    :return: dict of contents
    """

    try:
        with open('config/feed_config.yaml', 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
    except (yaml.YAMLError, FileNotFoundError) as error:
        current_app.logger.error('YAML read error %s', error)
        abort(500)

    return cfg


def feed_parse(url):
    """
    return mongodb cursor results from a find query

    :param url: the feed url to parse
    :returns: list
    """

    # parse the feed and get the results
    res = feedparser.parse(url)

    # check is parse returned with results
    if res.entries:
        return res.entries

    # no entries then error out, something went wrong
    current_app.logger.error('FEED parse error %s', url)

    return None


def get_gog_info(query):
    """
    query gog api

    :param query: query passed to the gog API
    :return: json of the query
    """
    gog_api_url = "https://embed.gog.com/games/ajax/filtered?"

    response = requests.get(gog_api_url + query)

    if response.status_code != 200:
        abort(500)

    return json.loads(response.content.decode('utf-8'))
