from flask import Blueprint, request, render_template
from models.user import User

main_views = Blueprint("main", __name__)

@main_views.get("/", strict_slashes=False)
def index():
    return render_template("index.html")

@main_views.get("/profile/<string:username>", strict_slashes=False)
def profile(username):
    user = User.find_by_username(username)
    return render_template("profile.html", user=user)
