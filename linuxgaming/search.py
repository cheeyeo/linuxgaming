from flask import (Blueprint, flash, redirect, url_for, render_template,
                   current_app)
from . import database

bp = Blueprint('search', __name__, url_prefix='/search')


@bp.route("/<path:path>", methods=["GET"])
def search(path):

    pages = ['game', 'twitch', 'youtube', 'article', 'podcast']
    if any(x in path for x in pages):
        result = database.find_all({"type": path})

        return render_template(
            'pages/search.html', entries=result, count=result.count())
    else:
        flash('1337 Hacks in progress...')
        current_app.logger.info('Manual search probe %s', path)

        return redirect(url_for('home'))
