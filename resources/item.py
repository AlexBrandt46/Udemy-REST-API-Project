""" File containing Blueprint and classes for handling /item HTTP requests """


import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    """ Class used to handle HTTP requests for the /item/item_id endpoint

    Args:
        MethodView (_type_): _description_
    """

    def get(self, item_id: str) -> tuple:
        """Performs GET request to retrieve a specific item
        
        Args:
            item_id (str): The id of the item to retrieve data of
        Returns:
            dict: Response message/data
            int: The status code of the response
        """

        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Store not found")


    def delete(self, item_id: str) -> tuple:
        """
            Performs DELETE request to delete an item
            
            Args:
                name (str): The name of the store to retrieve specific items from
            Returns:
                dict: Response message/data
                int: The status code of the response
        """
        try:
            del items[item_id]
            return { "message": "Item deleted." }
        except KeyError:
            abort(404, message="Item not found.")


    def put(self, item_id: str) -> tuple:
        """ Handles PUT request of /item endpoint

        Args:
            item_id (str): the item_id to update data of

        Returns:
            tuple: represents the HTTP response
        """
        item_data = request.get_json()

        if "price" not in item_data or "name" not in item_data:
            abort(400, message="Bad request. Ensure 'price' and 'name' " +
                "are included in the JSON payload.")

        try:
            # Does an inplace modification to the dictionary that updates the
            # values in item with those in the corresponding keys in item_data
            item = items[item_id]
            item |= item_data

            return item
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    """Class that handles the HTTP requests for the /item endpoint which handles all items

    Args:
        MethodView (_type_): _description_
    """

    def get(self) -> dict:
        """ Retrieves all items in the database

        Returns:
            dict: a dict containing all of the items
        """
        return { "items": list(items.values()) }


    def post(self) -> tuple:
        """Performs POST request to add an item using the store name in the URL
        
        Returns:
            dict: Response message
            int: The status code of the response
        """
        item_data = request.get_json()  # Grabs the incoming JSON from the request

        if (
            "price" not in item_data or
            "store_id" not in item_data or
            "name" not in item_data
        ):
            abort(400, message="Bad request. Ensure 'price', 'store_id', " +
                    "and 'name' are included in the JSON payload.")

        for item in items.values():
            if (
                item_data["name"] == item["name"] and
                item_data["store_id"] == item["store_id"]
            ):
                abort(400, message="Item already exists.")

        item_id = uuid.uuid4().hex
        item = { **item_data, "id": item_id }
        items[item_id] = item

        return item, 201
    