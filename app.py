"""_summary_
File contains API requests for stores
"""

import os

from flask import Flask
from flask_smorest import Api
# from flask_migrate import Migrate

from db import db
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

def create_app(db_url:str=None) -> Flask:
    """_summary_

    Args:
        db_url (str, optional): The URL of the database to use. Defaults to None.

    Returns:
        Flask: A Flask application
    """
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    # migrate = Migrate(app, db)

    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app
        