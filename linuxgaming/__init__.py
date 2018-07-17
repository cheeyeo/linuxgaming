from flask import render_template, Flask
from flask_compress import Compress
from flask_pymongo import PyMongo
from flask_htmlmin import HTMLMIN
from . import update
from . import details

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

    @app.route("/")
    def home():
        all_data = mongo.db.items.find().sort('date', -1)
        return render_template('pages/list.html', entries=all_data)

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error('internal error %s', error)
        return render_template(
            "message.html",
            icon="frown",
            msg="Something went wrong!"), 500

    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.info('page not found')
        return render_template(
            "message.html",
            icon="frown",
            msg="I think you are lost!"), 404

    return app
