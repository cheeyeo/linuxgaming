"""
shows more sources about the current sources.

:return: Blueprint
"""
from flask import (Blueprint, flash, redirect, render_template, url_for,
                   current_app)
from . import database
from . import util

BP = Blueprint('sources', __name__, url_prefix='/sources')


@BP.route("/all", methods=["GET"])
def sources_all():
    """display all sources"""

    feed_config = util.load_yaml()

    return render_template('pages/all_sources.html', data=feed_config)


@BP.route("/<path:path>", methods=["GET"])
def sources(path):
    """Source page"""
    feed_config = util.load_yaml()

    if path in feed_config:
        source_data = feed_config[path]
    else:
        flash('1337 Hacks in progress...')
        current_app.logger.info('Manual sources probe %s', path)
        return redirect(url_for('home'))

    source_items = database.find_all({"name": path})

    return render_template(
        'pages/sources.html', data=source_data, entries=source_items)
