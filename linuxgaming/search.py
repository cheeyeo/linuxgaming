from flask import (
    Blueprint,
    render_template,
    current_app)

bp = Blueprint('search', __name__, url_prefix='/search')


@bp.route("/twitch", methods=('GET', 'POST'))
def twitch():

    all_data = current_app.mongo.db.items.find(
        {"type": "twitch"}).sort('date', -1)
    return render_template(
        'pages/search.html',
        entries=all_data,
        count=all_data.count(),
        source="twitch")


@bp.route("/youtube", methods=('GET', 'POST'))
def youtube():

    all_data = current_app.mongo.db.items.find(
        {"type": "youtube"}).sort('date', -1)
    return render_template(
        'pages/search.html',
        entries=all_data,
        count=all_data.count(),
        source="youtube")


@bp.route("/article", methods=('GET', 'POST'))
def article():

    all_data = current_app.mongo.db.items.find(
        {"type": "article"}).sort('date', -1)
    return render_template(
        'pages/search.html',
        entries=all_data,
        count=all_data.count(),
        source="articles")


@bp.route("/podcast", methods=('GET', 'POST'))
def podcast():

    all_data = current_app.mongo.db.items.find(
        {"type": "podcast"}).sort('date', -1)
    return render_template(
        'pages/search.html',
        entries=all_data,
        count=all_data.count(),
        source="podcasts")


@bp.route("/gog", methods=('GET', 'POST'))
def gog():

    all_data = current_app.mongo.db.items.find(
        {"name": "gog"}).sort('date', -1)
    return render_template(
        'pages/search.html',
        entries=all_data,
        count=all_data.count(),
        source="gog")


@bp.route("/allthethings", methods=('GET', 'POST'))
def allthethings():

    all_data = current_app.mongo.db.items.find().sort('date', -1)
    return render_template(
        'pages/search.html',
        entries=all_data,
        count=all_data.count(),
        source="of all the things")
