""" File containing Blueprint and classes for handling /store HTTP requests """

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    """Class used for handling the /Store requests

    Args:
        MethodView: _description_
    """

    # TODO: Add description to 200 response code annotation
    @blp.response(200, StoreSchema)
    def get(self, store_id: int) -> tuple:
        """ GET request handler for the /store/store_id endpoint

        Args:
            store_id (int): The store_id of the desired store

        Returns:
            tuple: Contains the store info or an error code/message
        """
        store = StoreModel.query.get_or_404(store_id)
        return store


    @jwt_required
    def delete(self, store_id: int) -> tuple:
        """DELETE request handler for the /store/store_id endpoint

        Args:
            store_id (int): The store_id of the store that needs deletion

        Returns:
            tuple: Contains the response status code and response message
        """

        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privileges required.")

        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}

@blp.route("/store")
class StoreList(MethodView):
    """Class that handles the HTTP requests for the /store endpoint which handles all stores
 import jwt_required, get_jwt
    Args:
        MethodView (_type_): _description_
    """

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """Performs GET request to retrieve all stores
        
        Returns:
            dict: A dictionary containing a list of all stores
        """
        return StoreModel.query.all()

    # TODO: Add description to 200 response code annotation
    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        """Performs POST request to create a new store
        
        Returns:
            dict: The store that was created as part of this request
            int: The status code of the response
        """

        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, "A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store
