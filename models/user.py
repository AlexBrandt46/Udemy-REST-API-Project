""" Model file used to represent a user in the database """

from db import db

class UserModel(db.Model):
    """ Model class used to represent a user in the database """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    