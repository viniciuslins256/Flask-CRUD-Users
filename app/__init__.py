from app import views
from app.configurations import authentication
from app.configurations import database
from app.configurations import migration

from config import config_selector

from flask import Flask


def create_app(config_name="production"):
    app = Flask(__name__)
    app.config.from_object(config_selector[config_name])

    database.init_app(app)
    migration.init_app(app)
    authentication.init_app(app)
    views.init_app(app)

    return app
