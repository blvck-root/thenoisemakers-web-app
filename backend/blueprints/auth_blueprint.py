from flask import Blueprint, request, render_template, redirect, flash
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User


auth_views = Blueprint("auth", __name__)
users = User.collection


@auth_views.route("/register", strict_slashes=False, methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uploaded_file = request.files['picture']
        full_name = request.form.get("full_name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Save the uploaded file to a directory on your server
        # Preferably outside the application root
        uploaded_file.save(f"static/images/{uploaded_file.filename}")

        # Implement database logic to register user
        data = {
            "full_name": full_name,
            "username": username,
            "email": email,
            "password": generate_password_hash(password),
            "profile_pic": f"static/images/{uploaded_file.filename}"
        }

        try:
            check_email = User.find_by_email(email)
            check_username = User.find_by_username(username)

            if check_email or check_username:
                flash("Credentials already in use!", "error")
                return redirect("/login")
            
            new_user = User(**data)
            new_user.save()
        except Exception as e:
            print(e)
            flash("Error occurred during registration. Try again!", "error")
            return redirect("/register")

        return render_template("login.html")
    
    # Render template for GET requests
    return render_template("register.html")


@auth_views.route("/login", strict_slashes=False, methods=["GET", "POST"])
def login():
    # Define application logic for profile page
    # If a user already exists and tries to be funny by
    # manually entering the /login route, they should be
    # redirected to the index page
    if current_user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        # Enter the logic for processing registration
    
        username = request.form.get("username")
        user_password = request.form.get("password")

        # Retrieve user from the database with username
        find_user = User.find_by_username(username)

        if find_user == None:
            flash("Invalid login credentials!", "error")
            return redirect("/login")
        
        # compare the user password with the password returned from db
        is_valid_password = check_password_hash(find_user.get("password"), user_password)

        if not is_valid_password:
            flash("Invalid login credentials!", "error")
            return redirect("/login")
        
        # At this point all is well; so instantiate the User class 
        # This is to enable the Flask-Login Extension kick in
        log_user = User(
            find_user.get("full_name"),
            find_user.get("username"),
            find_user.get("email"),
            find_user.get("password"),
            find_user.get("_id"),
            find_user.get("bio"),
            find_user.get("links"),
            find_user.get("profile_pic"),
            find_user.get("banner_img") 
        )

        # use the login_user function imported from flask_login
        login_user(log_user)

        # Then return the user to the index page after sucess
        return redirect(f"/profile/{username}")

        # Make sure to do proper error handling with try/except
        # I don't want to make the code too bulky
 
    # for GET request to the route, we sent the html form
    return render_template("login.html")


# Create Sign Out Route which we'll create a button for
@auth_views.route("/logout", strict_slashes=False)
@login_required
def logout():
    # We wrap the logout function with @login_required decorator
    # So that only logged in users should be able to 'log out'
    logout_user()
    return redirect("/")
