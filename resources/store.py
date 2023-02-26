""" File containing Blueprint and classes for handling /store HTTP requests """

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import StoreSchema
from db import db
from models import StoreModel

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    """Class used for handling the /Store requests

    Args:
        MethodView: _description_
    """

    @blp.response(200, StoreSchema)
    def get(self, store_id: str) -> tuple:
        """ GET request handler for the /store/store_id endpoint

        Args:
            store_id (str): The store_id of the desired store

        Returns:
            tuple: Contains the store info or an error code/message
        """
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")


    def delete(self, store_id: str) -> tuple:
        """DELETE request handler for the /store/store_id endpoint

        Args:
            store_id (str): The store_id of the store that needs deletion

        Returns:
            tuple: Contains the response status code and response message
        """
        try:
            del stores[store_id]
            return { "message": "Store deleted." }
        except KeyError:
            abort(404, message="Store not found.")


    def put(self, store_id: str) -> tuple:
        """ PUT request handler for the /store/store_id endpoint to update individual stores

        Args:
            store_id (str): The store id to use to update store data

        Returns:
            tuple: The updated store and a status code, or a message and a status code
        """
        store_data = request.get_json()

        if "name" not in store_data:
            abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")

        try:
            store = stores[store_id]
            store |= store_data

            return store
        except KeyError:
            abort(404, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    """Class that handles the HTTP requests for the /store endpoint which handles all stores

    Args:
        MethodView (_type_): _description_
    """

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """Performs GET request to retrieve all stores
        
        Returns:
            dict: A dictionary containing a list of all stores
        """
        return stores.values()


    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        """Performs POST request to create a new store
        
        Returns:
            dict: The store that was created as part of this request
            int: The status code of the response
        """

        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, "A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store
