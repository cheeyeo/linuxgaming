"""
module to search database based on the path.

"""
from flask import (Blueprint, flash, redirect, url_for, render_template,
                   current_app)
from . import database

BP = Blueprint('search', __name__, url_prefix='/search')


@BP.route("/<path:path>", methods=["GET"])
def search(path):
    """
    search database based on the given path

    :param path: path is used as the db find
    :return: Flask render_template
    """
    # pages that we allow
    pages = ['game', 'twitch', 'youtube', 'article', 'podcast']
    # if they are not in the path, then redirect.
    if any(x in path for x in pages):
        result = database.find_all({"type": path})

        return render_template(
            'pages/search.html', entries=result, count=result.count())

    flash('1337 Hacks in progress...')
    current_app.logger.info('Manual search probe %s', path)

    return redirect(url_for('home'))
