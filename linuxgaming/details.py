from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
    current_app)
import yaml

bp = Blueprint('details', __name__, url_prefix='/details')


def load():
    """Return the YAML parsed config file."""
    try:
        with open('config/feed_config.yaml', 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
    except yaml.YAMLError as exc:
        current_app.logger.error('YAML read error %s', exc)

    return cfg


@bp.route("/<path:path>", methods=('GET', 'POST'))
def details(path):
    """Source details page"""
    feed_config = load()

    if path in feed_config:
        source_data = feed_config[path]
    else:
        flash('1337 Hacks in progress...')
        current_app.logger.info('Manual details probe %s', path)
        return redirect(url_for('home'))

    source_items = current_app.mongo.db.items.find(
        {"name": path}).sort('date', -1)

    return render_template(
        'pages/details.html',
        data=source_data,
        items=source_items)
