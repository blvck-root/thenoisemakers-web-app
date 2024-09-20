"""Setting up my flask app."""

from flask import Flask
from blueprints.main_blueprint import main_views
from blueprints.auth_blueprint import auth_views

from flask_login import LoginManager
from models.user import User
from flask_wtf import CSRFProtect

app = Flask(__name__, template_folder="../templates")
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
    cur_user = User.find_by_id(id)

    if cur_user is None:
        return None
    
    # create user instance from retrieved user
    return User(
        cur_user.get("full_name"),
        cur_user.get("username"),
        cur_user.get("email"),
        cur_user.get("password"),
        cur_user.get("bio"),
        cur_user.get("links"),
        cur_user.get("profile_pic"),
        cur_user.get("banner_img")
    )

if __name__ == '__main__':
    app.run(debug=True)
