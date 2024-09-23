from flask import Blueprint, request, render_template, send_from_directory

main_views = Blueprint("main", __name__)

@main_views.get("/", strict_slashes=False)
def index():
    return render_template("index.html")

@main_views.get("/profile/<string:username>", strict_slashes=False)
def profile(username):
    return render_template("profile.html")
