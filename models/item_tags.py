""" Model file used to represent an item tag in the database """

from db import db

class ItemTags(db.Model):
    """ Model class used to represent an item tag in the database """

    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
    