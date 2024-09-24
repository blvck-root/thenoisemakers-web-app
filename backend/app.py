"""Setting up my flask app."""

from flask import Flask
from bson import ObjectId
from blueprints.main_blueprint import main_views
from blueprints.auth_blueprint import auth_views

from flask_login import LoginManager
from models.user import User
from flask_wtf import CSRFProtect

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config.from_object('config')
app.secret_key = "makesomenoise"
csrf = CSRFProtect(app)

app.register_blueprint(main_views)
app.register_blueprint(auth_views)

login = LoginManager(app)
login.login_view = "/login"

@login.user_loader
def load_user(id):
    """Confirm user exists then use, else return None"""
    print(f"ID: {id}")
    current_user = User.find_by_id(ObjectId(id))

    if current_user is None:
        print("No user!!!")
        return None
    
    # create user instance from retrieved user
    return User(
        current_user.get("full_name"),
        current_user.get("username"),
        current_user.get("email"),
        current_user.get("password"),
        current_user.get("_id"),
        current_user.get("bio"),
        current_user.get("links"),
        current_user.get("profile_pic"),
        current_user.get("banner_img")
    )

if __name__ == '__main__':
    app.run(debug=True)
