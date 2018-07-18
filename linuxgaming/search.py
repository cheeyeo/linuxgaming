from flask import (
    Blueprint,
    flash,
    redirect,
    url_for,
    render_template,
    current_app)

bp = Blueprint('search', __name__, url_prefix='/search')


@bp.route("/<path:path>", methods=('GET', 'POST'))
def test(path):

    pages = ['gog', 'twitch', 'youtube', 'article', 'podcast', 'allthethings']
    if any(x in path for x in pages):
        result = current_app.mongo.db.items.find(
            {"type": path}).sort('date', -1)
        return render_template(
            'pages/search.html',
            entries=result,
            count=result.count())
    else:
        flash('1337 Hacks in progress...')
        current_app.logger.info('Manual search probe %s', path)
        return redirect(url_for('home'))
