from flask import render_template, Flask
from flask_compress import Compress
from flask_pymongo import PyMongo
from flask_htmlmin import HTMLMIN
from datetime import datetime, timedelta

import dateutil.parser
from . import update
from . import details
from . import search
from . import database

compress = Compress()


def create_app():
    # create and configure the app

    app = Flask(__name__, static_url_path='/static')
    app.config.from_object('config')

    # page performance tweeks
    app.config['MINIFY_PAGE'] = True
    compress.init_app(app)
    HTMLMIN(app)

    # db init
    mongo = PyMongo(app)
    app.mongo = mongo

    # register blueprint modules
    app.register_blueprint(update.bp)
    app.register_blueprint(details.bp)
    app.register_blueprint(search.bp)

    @app.route("/")
    def home():
        result = database.find_all({
            "date": {
                '$gte': datetime.now() - timedelta(hours=24)
            }
        })
        return render_template('pages/home.html', entries=result)

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error('internal error %s', error)
        return render_template(
            "message.html", icon="frown", msg="Something went wrong!"), 500

    @app.errorhandler(404)
    def page_not_found():
        app.logger.info('page not found')
        return render_template(
            "message.html", icon="frown", msg="I think you are lost!"), 404

    @app.template_filter('strftime')
    def _jinja2_filter_datetime(date):
        date = dateutil.parser.parse(str(date))
        native = date.replace(tzinfo=None)
        format = '%a %d %b %X %Y'
        return native.strftime(format)

    return app
