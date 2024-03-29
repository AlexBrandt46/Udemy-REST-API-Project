from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")

@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    """ Class that handles endpoints for the tags of specific stores """

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id: int):
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()

    # TODO: Add description to the blp response 201 object
    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):

        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privileges required.")

        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as error:
            abort(500, message=str(error))

        return tag


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    """ Class to handle endpoints for the tags related to an item """

    # TODO: Add description to the blp response 201 object
    @jwt_required()
    @blp.response(201, TagSchema)
    def post(self, item_id: int, tag_id: int):

        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privileges required.")

        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag

    # TODO: Add description to the blp response 200 object
    @jwt_required()
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):

        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privileges required.")

        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while removing the tag.")

        return {"message": "Item removed from tag", "item": item, "tag": tag}

@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    """ Class to handle endpoints for creating actual tags """

    # TODO: Add description to 200 response code annotation
    @blp.response(200, TagSchema)
    def get(self, tag_id: int):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @jwt_required()
    @blp.response(202, description="Deletes a tag if no item is tagged with it.",
                  example={"message": "Tag deleted."})
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(400, description="Returned if the tag is assigned to one or more items." +
                    "In this case, the tag is not deleted.")
    def delete(self, tag_id: int):

        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privileges required.")

        tag = TagModel.query.get_or_404(tag_id)

        # Checks if the items list associated with this tag is empty
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}

        abort(400, message="Could not delete tag. Make sure tag is not associated" +
            "with any items, then try again.")
