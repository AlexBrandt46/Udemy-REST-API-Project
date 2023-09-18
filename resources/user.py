""" File containing Blueprint and HTTP request handlers for User model """

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity

from db import db
from models import UserModel
from schemas import UserSchema
from blocklist import BLOCKLIST


blp = Blueprint("Users", "users", description="Operations on users.")

@blp.route("/register")
class UserRegister(MethodView):
    """ Class used to handle HTTP requests for the /register endpoint

    Args:
        MethodView (_type_): _description_
    """

    @blp.arguments(UserSchema)
    def post(self, user_data: dict):
        """ Performs POST request to create a user
        
        Args:
            user_data (dict): Information about the new user containing the username and password
        Returns:
            dict: Response message/data
            int: The status code of the response
        """

        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        user = UserModel(
            username = user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )

        db.session.add(user)
        db.session.commit()

        return { "message": "User created successfully." }, 201


@blp.route("/user/<int:user_id>")
class User(MethodView):
    """ Class used to handle HTTP requests for the /user/user_id endpoint """

    # TODO: Add description to 200 response code annotation
    @blp.response(200, UserSchema)
    def get(self, user_id: int) -> UserSchema:
        """ GET request that retrieves information about the user with the user_id passed
        in as an argument

        Args:
            user_id (int): The unique ID of the user whose information is being searched for

        Returns:
            UserSchema: UserSchema object containing the ID and username of the user with the
            given ID
        """

        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required()
    def delete(self, user_id: int) -> dict:
        """ DELETE request that removes the user with the passed in ID

        Args:
            user_id (int): The unique ID of the user who's being removed from the database

        Returns:
            dict: Object with a message verifying the user was successfully deleted
        """

        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        user = UserModel.query.get_or_404(user_id)

        if user.id == user_id:
            abort(405, message="User cannot delete themselves")

        db.session.delete(user)
        db.session.commit()

        return { "message": "User deleted." }, 200


@blp.route("/login")
class UserLogin(MethodView):
    """ Class used to handle HTTP requests for the /login endpoint """

    @blp.arguments(UserSchema)
    def post(self, user_data: dict) -> dict:
        """ POST request to log the user in

        Args:
            user_data (dict): Dictionary containing the user's login info

        Returns:
            dict: A dictionary containing the user's access token and refresh token
        """

        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return { "access_token": access_token, "refresh_token": refresh_token }
        else:
            abort(401, message="Invalid credentials.")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    """ Class that handles HTTP requests for the /refresh endpoint """
    @jwt_required(refresh=True)
    def post(self):
        " POST request to refresh the user's access token "
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return { "access_token": new_token }

@blp.route("/logout")
class UserLogout(MethodView):
    """ Class used to handle HTTP requests for the /logout endpoint """

    @jwt_required()
    def post(self):
        """ POST request to log the user out

        Returns:
            JSON object containing a message that the user has logged out
        """
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}
