"""
Main application

"""
from datetime import datetime, timedelta
from flask import render_template, Flask
from flask_compress import Compress
from flask_pymongo import PyMongo
from flask_htmlmin import HTMLMIN

import dateutil.parser
from . import update
from . import details
from . import search
from . import database

COMPRESS = Compress()


def create_app():
    """ Create the Flask application """

    app = Flask(__name__, static_url_path='/static')
    app.config.from_object('config')

    # page performance tweeks
    app.config['MINIFY_PAGE'] = True
    COMPRESS.init_app(app)
    HTMLMIN(app)

    # db init
    mongo = PyMongo(app)
    app.mongo = mongo

    # register blueprint modules
    app.register_blueprint(update.BP)
    app.register_blueprint(details.BP)
    app.register_blueprint(search.BP)

    @app.route("/")
    def home():
        result = database.find_all({
            "date": {
                '$gte': datetime.now() - timedelta(hours=48)
            }
        })
        return render_template('pages/home.html', entries=result)

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error('internal error %s', error)
        return render_template(
            "message.html", msg="Something went wrong!"), 500

    @app.errorhandler(404)
    def page_not_found(page):
        app.logger.info('page not found %s', page)
        return render_template(
            "message.html", msg="I think you are lost!"), 404

    @app.template_filter('strftime')
    def _jinja2_filter_datetime(date):
        date = dateutil.parser.parse(str(date))
        native = date.replace(tzinfo=None)
        new_format = '%a %d %b %X %Y'
        return native.strftime(new_format)

    return app
