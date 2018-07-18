from googleapiclient.discovery import build
from twitch import TwitchClient
from flask import Blueprint, render_template, current_app
from . import database
import json
import requests
import feedparser
import dateutil.parser
from . import util

bp = Blueprint('update', __name__, url_prefix='/update')


def parse(url):
    return feedparser.parse(url).entries


@bp.route('/rss', methods=["GET"])
def rss_update():

    feed_config = util.load_yaml()

    for section in feed_config:
        if 'rss' not in feed_config[section]:
            continue

        current_app.logger.info('[RSS] Updating %s', section)
        feeds = parse(feed_config[section]['rss']['url'])

        for feed in feeds:

            trimtitle = feed.title[0:150]

            if not hasattr(feed, 'description'):
                description = ""
            else:
                description = feed.description

            data = {
                "name": section,
                "icon": feed_config[section]['icon'],
                "title": trimtitle,
                "description": description,
                "url": feed.link,
                "type": feed_config[section]['rss']['type'],
                "date": dateutil.parser.parse(feed.updated)
            }

            database.replace_one({'title': trimtitle}, data)

    return render_template("message.html", msg="RSS feeds updated!")


@bp.route('/twitch', methods=["GET"])
def twitch_update():

    feed_config = util.load_yaml()

    for section in feed_config:
        if 'twitch' not in feed_config[section]:
            continue

        current_app.logger.info('[TWITCH] Updating %s', section)
        twitch_channelid = feed_config[section]['twitch']['twitch_id']

        client = TwitchClient(
            client_id=current_app.config['TWITCH_CLIENTID'],
            oauth_token=current_app.config['TWITCH_TOKEN'])

        videos = client.channels.get_videos(
            twitch_channelid,  # Channel ID
            10,  # Limit
            0,  # Offset
            'archive',  # Broadcast type
            'en',  # Lang
            'time',  # Sort
        )

        for search_results in videos:
            trimtitle = search_results['title'][0:150]
            data = {
                "name": section,
                "icon": feed_config[section]['icon'],
                "title": trimtitle,
                "description": search_results['description'],
                "url": search_results['url'],
                "type": "twitch",
                "date": dateutil.parser.parse(search_results['recorded_at'])
            }

            database.replace_one({'url': search_results['url']}, data)

    return render_template("message.html", msg="Twitch API updated!")


@bp.route('/youtube', methods=["GET"])
def youtube_update():

    key = current_app.config['YOUTUBE_APIKEY']
    youtube_api = 'youtube'
    api_version = 'v3'

    feed_config = util.load_yaml()

    for section in feed_config:
        if 'youtube' not in feed_config[section]:
            continue

        youtube_channel_id = feed_config[section]['youtube']['channel_id']

        youtube = build(youtube_api, api_version, developerKey=key)

        current_app.logger.info('[YOUTUBE] Updating %s', section)
        search_response = youtube.search().list(
            q="",
            channelId=youtube_channel_id,
            part='id,snippet',
            order='date',
            maxResults=5).execute()

        for search_result in search_response.get('items', []):
            trimtitle = search_result['snippet']['title'][0:150]
            if search_result['id']['kind'] == 'youtube#video':
                data = {
                    "name":
                    section,
                    "icon":
                    feed_config[section]['icon'],
                    "title":
                    trimtitle,
                    "description":
                    search_result['snippet']['description'],
                    "type":
                    "youtube",
                    "url":
                    "https://www.youtube.com/watch?v=" +
                    search_result['id']['videoId'],
                    "date":
                    dateutil.parser.parse(
                        search_result['snippet']['publishedAt'])
                }

                database.replace_one({'title': trimtitle}, data)

    return render_template("message.html", msg="Youtube API updated!")


@bp.route('/gog', methods=["GET"])
def gog_update():

    from datetime import datetime

    count = 1
    while count < 51:
        query = "mediaType=game&system=Linux&limit=50&page=" + str(count)
        game_data = get_gog_info(query)
        if game_data is None:
            return render_template("message.html", msg="GoG query error")

        for search_result in game_data['products']:

            if not search_result['worksOn']['Linux']:
                continue

            if not search_result['buyable']:
                continue

            if search_result['isComingSoon']:
                continue

            if "Soundtrack" in search_result['title']:
                continue

            if search_result['releaseDate']:
                release_date = datetime.fromtimestamp(
                    search_result['releaseDate']).isoformat()
            else:
                release_date = datetime.fromtimestamp(
                    search_result['salesVisibility']['from']).isoformat()

            data = {
                "name": "gog",
                "icon": "gog.png",
                "type": "game",
                "title": search_result['title'],
                "image": "https:" + search_result['image'] + ".png",
                "publisher": search_result['publisher'],
                "category": search_result['category'],
                "url": "https://www.gog.com" + search_result['url'],
                "date": dateutil.parser.parse(release_date)
            }

            database.replace_one({'title': search_result['title']}, data)

        count = count + 1

    return render_template(
        "message.html", icon="smile", msg="GoG games updated!")


def get_gog_info(query):

    gog_api_url = "https://embed.gog.com/games/ajax/filtered?"

    response = requests.get(gog_api_url + query)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
