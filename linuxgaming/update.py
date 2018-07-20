"""
module for updating various sources.

"""
from googleapiclient.discovery import build
from twitch import TwitchClient
from flask import Blueprint, render_template, current_app
import dateutil.parser
from . import database
from . import util

BP = Blueprint('update', __name__, url_prefix='/update')


@BP.route('/rss', methods=["GET"])
def rss_update():
    """
    update sources with rss feeds

    :return: Flask render_template
    """

    # load sources config
    feed_config = util.load_yaml()

    for section in feed_config:
        # if it does not have an rss section skip
        if 'rss' not in feed_config[section]:
            continue

        current_app.logger.info('[RSS] Updating %s', section)

        # parse the source url rss feed
        feeds = util.feed_parse(feed_config[section]['rss']['url'])

        # check for errors
        if feeds is None:
            continue

        for feed in feeds:

            # if not title, then just skip
            if hasattr(feed, 'title'):
                trimmed_title = feed.title[0:150]
            else:
                continue

            # some feeds dont have a description, RSS 2.0
            if not hasattr(feed, 'description'):
                description = ""
            else:
                description = feed.description

            # construct db item
            data = {
                "name": section,
                "title": trimmed_title,
                "description": description,
                "url": feed.link,
                "type": feed_config[section]['rss']['type'],
                "date": dateutil.parser.parse(feed.updated)
            }

            # insert based on title
            database.replace_one({'title': trimmed_title}, data)

    return render_template("message.html", msg="RSS feeds updated!")


@BP.route('/twitch', methods=["GET"])
def twitch_update():
    """
    update sources with twitch API

    :return: Flask render_template
    """

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
            trimmed_title = search_results['title'][0:150]
            data = {
                "name": section,
                "title": trimmed_title,
                "description": search_results['description'],
                "url": search_results['url'],
                "type": "twitch",
                "date": dateutil.parser.parse(search_results['recorded_at'])
            }

            database.replace_one({'url': search_results['url']}, data)

    return render_template("message.html", msg="Twitch API updated!")


@BP.route('/youtube', methods=["GET"])
def youtube_update():
    """
    update sources with youtube API

    :return: Flask render_template
    """
    feed_config = util.load_yaml()

    for section in feed_config:
        if 'youtube' not in feed_config[section]:
            continue

        youtube_channel_id = feed_config[section]['youtube']['channel_id']

        youtube = build(
            'youtube', 'v3', developerKey=current_app.config['YOUTUBE_APIKEY'])

        current_app.logger.info('[YOUTUBE] Updating %s', section)

        search_response = youtube.search().list(
            q="",
            channelId=youtube_channel_id,
            part='id,snippet',
            order='date',
            maxResults=5).execute()

        for search_result in search_response.get('items', []):
            trimmed_title = search_result['snippet']['title'][0:150]
            data = {
                "name":
                section,
                "title":
                trimmed_title,
                "description":
                search_result['snippet']['description'],
                "type":
                "youtube",
                "url":
                "https://www.youtube.com/watch?v=" +
                search_result['id']['videoId'],
                "date":
                dateutil.parser.parse(search_result['snippet']['publishedAt'])
            }

            database.replace_one({'title': trimmed_title}, data)

    return render_template("message.html", msg="Youtube API updated!")


@BP.route('/gog', methods=["GET"])
def gog_update():
    """
    update GoG games via API

    :return: Flask render_template
    """
    from datetime import datetime

    count = 1
    while count < 51:
        query = "mediaType=game&system=Linux&limit=50&page=" + str(count)
        game_data = util.get_gog_info(query)

        for search_result in game_data['products']:
            # GoG API is an arse are returns loads of entries that we
            # dont want so all of the following if statements are to
            # filter them out
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
                "name": "GoG",
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
