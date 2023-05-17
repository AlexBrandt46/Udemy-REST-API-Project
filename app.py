"""_summary_
File contains API requests for stores
"""

import os
import secrets

from flask import Flask, jsonify
from flask_smorest import Api
# from flask_migrate import Migrate

from db import db
from blocklist import BLOCKLIST
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from flask_jwt_extended import JWTManager

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
    
    app.config["JWT_SECRET_KEY"] = "236520528094713753437932268324630142015"
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        """Runs whenever we receive a JWT and checks if the token is in the blocklist, if it is, then the request is terminated and it is revoked

        Args:
            jwt_header (_type_): _description_
            jwt_payload (_type_): _description_

        Returns:
            _type_: _description_
        """
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """Event handler that returns an error to the user in the event that check_if_token_in_blocklist returns true

        Args:
            jwt_header (_type_): _description_
            jwt_payload (_type_): _description_
        """
        return(
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ), 401
        )
    
    # Add a claim to a JWT
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # Purely for learning purposes, normally would check in database for a user's permissions
        if identity == 1:
            return { "is_admin": True }
        
        return { "is_admin": False }
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "message": "The token is expired.",
                "error": "token_expired"
            }), 401
        )
        
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({
                "message": "Signature verification failed.",
                "error": "invalid_token"
            }), 401
        )
        
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({
                "description": "Request does not contain an access token.",
                "error": "authorization_required"
            }), 401
        )

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
        