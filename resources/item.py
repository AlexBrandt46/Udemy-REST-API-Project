""" File containing Blueprint and classes for handling /item HTTP requests """

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    """ Class used to handle HTTP requests for the /item/item_id endpoint

    Args:
        MethodView (_type_): _description_
    """

    @blp.response(200, ItemSchema)
    def get(self, item_id: int) -> tuple:
        """Performs GET request to retrieve a specific item
        
        Args:
            item_id (int): The id of the item to retrieve data of
        Returns:
            dict: Response message/data
            int: The status code of the response
        """
        item = ItemModel.query.get_or_404(item_id)
        return item


    def delete(self, item_id: int) -> tuple:
        """
            Performs DELETE request to delete an item
            
            Args:
                name (int): The name of the store to retrieve specific items from
            Returns:
                dict: Response message/data
                int: The status code of the response
        """
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data: dict, item_id: int) -> tuple:
        """ Handles PUT request of /item endpoint

        Args:
            item_id (int): the item_id to update data of
            item_data (dict): data to update the corresponding item with

        Returns:
            tuple: represents the HTTP response
        """
        item = ItemModel.query.get(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    """Class that handles the HTTP requests for the /item endpoint which handles all items

    Args:
        MethodView (_type_): _description_
    """
    @blp.response(200, ItemSchema(many=True))
    def get(self) -> dict:
        """ Retrieves all items in the database

        Returns:
            dict: a dict containing all of the items
        """
        return ItemModel.query.all()


    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data) -> tuple:
        """Performs POST request to add an item using the store name in the URL
        
        Returns:
            dict: Response message
            int: The status code of the response
        """
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()  # writes item to data.db
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item
    