from googleapiclient.discovery import build
from twitch import TwitchClient
from flask import Blueprint, render_template, current_app
import yaml
import feedparser
import dateutil.parser

bp = Blueprint('update', __name__, url_prefix='/update')


def load():

    with open('config/feed_config.yaml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    return cfg


def parse(url):
    return feedparser.parse(url).entries


@bp.route('/rss', methods=('GET', 'POST'))
def rss_update():

    feed_config = load()

    for section in feed_config:
        if 'rss' not in feed_config[section]:
            continue

        print("Updating - " + section)
        feeds = parse(feed_config[section]['rss']['url'])

        for feed in feeds:

            trimtitle = feed.title[0:150]

            if not hasattr(feed, 'description'):
                description = ""
            else:
                description = feed.description
            data = {"name": section,
                    "icon": feed_config[section]['icon'],
                    "title": trimtitle,
                    "description": description,
                    "url": feed.link,
                    "type": feed_config[section]['rss']['type'],
                    "date": dateutil.parser.parse(feed.updated)}

            try:
                current_app.mongo.db.items.replace_one(
                    {'title': trimtitle}, data, True)
            except Exception as e:
                current_app.logger.error('DB replace error %s', e)
                return render_template(
                    "message.html", icon="frown", msg=str(e))

    return render_template(
        "message.html",
        icon="smile",
        msg="RSS feeds updated!")


@bp.route('/twitch', methods=('GET', 'POST'))
def twitch_update():

    feed_config = load()

    for section in feed_config:
        if 'twitch' not in feed_config[section]:
            continue

        print("Updating " + section)
        twitch_channelID = feed_config[section]['twitch']['twitch_id']

        client = TwitchClient(
            client_id=current_app.config['TWITCH_CLIENTID'],
            oauth_token=current_app.config['TWITCH_TOKEN']
        )

        videos = client.channels.get_videos(
            twitch_channelID,  # Channel ID
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

            try:
                current_app.mongo.db.items.replace_one(
                    {'url': search_results['url']}, data, True)
            except Exception as e:
                current_app.logger.error('DB replace error %s', e)
                return render_template(
                    "message.html", icon="frown", msg=str(e))

    return render_template(
        "message.html",
        icon="smile",
        msg="Twitch API updated!")


@bp.route('/youtube', methods=('GET', 'POST'))
def youtube_update():

    DEVELOPER_KEY = current_app.config['YOUTUBE_APIKEY']
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    feed_config = load()

    for section in feed_config:
        if 'youtube' not in feed_config[section]:
            continue

        youtube_channelID = feed_config[section]['youtube']['channel_id']

        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey=DEVELOPER_KEY)

        print("Updating - " + section)
        search_response = youtube.search().list(
            q="",
            channelId=youtube_channelID,
            part='id,snippet',
            maxResults=40
        ).execute()

        for search_result in search_response.get('items', []):
            trimtitle = search_result['snippet']['title'][0:150]
            if search_result['id']['kind'] == 'youtube#video':
                data = {
                    "name": section,
                    "icon": feed_config[section]['icon'],
                    "title": trimtitle,
                    "description": search_result['snippet']['description'],
                    "type": "youtube",
                    "url": "https://www.youtube.com/watch?v=" +
                    search_result['id']['videoId'],
                    "date": dateutil.parser.parse(
                        search_result['snippet']['publishedAt'])}

            try:
                current_app.mongo.db.items.replace_one(
                    {'title': trimtitle}, data, True)
            except Exception as e:
                current_app.logger.error('DB replace error %s', e)
                return render_template(
                    "message.html", icon="frown", msg=str(e))

    return render_template(
        "message.html",
        icon="smile",
        msg="Youtube API updated!")

#
# This GoG import is just so nasty and needs fixed, Will
# be enabling it until it is.
#


@bp.route('/gog', methods=('GET', 'POST'))
def gog_update():

    from datetime import datetime

    count = 1
    while count < 51:
        query = "mediaType=game&system=Linux&limit=50&page=" + str(count)
        game_data = get_gog_info(query)
        if game_data is None:
            return render_template(
                "message.html",
                icon="frown",
                msg="GoG query error")

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
                "type": "gog",
                "title": search_result['title'],
                "image": "https:" + search_result['image'] + ".png",
                "publisher": search_result['publisher'],
                "category": search_result['category'],
                "url": "https://www.gog.com" + search_result['url'],
                "date": dateutil.parser.parse(release_date)}

            try:
                current_app.mongo.db.items.replace_one(
                    {'title': search_result['title']}, data, True)
            except Exception as e:
                return render_template(
                    "message.html", icon="frown", msg=str(e))

        count = count + 1

    return render_template(
        "message.html",
        icon="smile",
        msg="GoG games updated!")


def get_gog_info(query):

    import json
    import requests

    GOG_API_URL = "https://embed.gog.com/games/ajax/filtered?"

    response = requests.get(GOG_API_URL + query)

    if response.status_code == 200:
        return (json.loads(response.content.decode('utf-8')))
    else:
        return None
