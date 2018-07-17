from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
    current_app)
import yaml

bp = Blueprint('search', __name__, url_prefix='/search')


def load():
    """Return the YAML parsed config file."""
    try:
        with open('config/feed_config.yaml', 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
    except yaml.YAMLError as exc:
        current_app.logger.error('YAML read error %s', exc)

    return cfg


@bp.route("/twitch", methods=('GET', 'POST'))
def twitch():

    all_data = current_app.mongo.db.items.find({"type" : "twitch"}).sort('date', -1)
    return render_template('pages/search.html', entries=all_data, count=all_data.count(), source="twitch")

@bp.route("/youtube", methods=('GET', 'POST'))
def youtube():

    all_data = current_app.mongo.db.items.find({"type" : "youtube"}).sort('date', -1)
    return render_template('pages/search.html', entries=all_data, count=all_data.count(), source="youtube")

@bp.route("/article", methods=('GET', 'POST'))
def article():

    all_data = current_app.mongo.db.items.find({"type" : "article"}).sort('date', -1)
    return render_template('pages/search.html', entries=all_data, count=all_data.count(), source="articles")


@bp.route("/podcast", methods=('GET', 'POST'))
def podcast():

    all_data = current_app.mongo.db.items.find({"type" : "podcast"}).sort('date', -1)
    return render_template('pages/search.html', entries=all_data, count=all_data.count(), source="podcasts")

@bp.route("/allthethings", methods=('GET', 'POST'))
def allthethings():

    all_data = current_app.mongo.db.items.find().sort('date', -1)
    return render_template('pages/search.html', entries=all_data, count=all_data.count(), source="of all the things")