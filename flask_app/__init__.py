from flask import Flask

from config import FLASK_DEBUG

from . import db_manager

from .routes import bp


def create_app():
    app = Flask(__name__)
    app.debug = FLASK_DEBUG
    app.register_blueprint(bp)
    db_manager.create_bd()

    return app