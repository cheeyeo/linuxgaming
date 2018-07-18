from flask import (Blueprint, flash, redirect, render_template, url_for,
                   current_app)
from . import database
from . import util

bp = Blueprint('details', __name__, url_prefix='/details')


@bp.route("/<path:path>", methods=["GET"])
def details(path):
    """Source details page"""
    feed_config = util.load_yaml()

    if path in feed_config:
        source_data = feed_config[path]
    else:
        flash('1337 Hacks in progress...')
        current_app.logger.info('Manual details probe %s', path)
        return redirect(url_for('home'))

    source_items = database.find_all({"name": path})

    return render_template(
        'pages/details.html', data=source_data, items=source_items)
