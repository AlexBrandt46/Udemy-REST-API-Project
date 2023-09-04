""" Model file used to represent an item in the database """

from db import db

class StoreModel(db.Model):
    """ Model class used to represent an item in the database """

    __tablename__ = "stores"

    # lazy='dynamic' makes sure the db doesn't retrieve these items until it's called

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populates="store",
                            lazy="dynamic", cascade="all, delete")
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
    