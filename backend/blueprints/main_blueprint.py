import json
import base64

from flask import Blueprint, request, render_template
from models.user import User
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, bytes):
            return base64.b64encode(o).decode('utf-8')
        return super().default(o)


main_views = Blueprint("main", __name__)

@main_views.get("/", strict_slashes=False)
def index():
    return render_template("index.html")

@main_views.get("/profile/<string:username>", strict_slashes=False)
def profile(username):
    user = User.find_by_username(username)
    return render_template("profile.html", user=user)

@main_views.get("/users", strict_slashes=False)
def get_users():
    users = User.find_all_users()
    return JSONEncoder().encode(users)

@main_views.delete("/users/<user_id>", strict_slashes=False)
def delete_user_by_id(user_id):
    result = User.collection.find_one_and_delete({'_id': ObjectId(user_id)})

    if result:
        print(result)
        return JSONEncoder().encode(
            {'message': "User deleted successfully"}
        ), 200
    return JSONEncoder().encode(
        {'message': "User not found"}
    ), 200
