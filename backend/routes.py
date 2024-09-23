"""
import json
import base64

from flask import jsonify, request, render_template
from bson import ObjectId

from app import app, csrf
from models.user import User, RegistrationForm, UpdateUserForm

users = User.collection


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, bytes):
            return base64.b64encode(o).decode('utf-8')
        return super().default(o)


# implement logic to display home page
@app.route('/')
def hello_noisemakers():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate():
        data = {
            'full_name': request.form.get('full_name'),
            'username': request.form.get('username'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
        }
        new_user = User(**data)
        new_user.save()
        return JSONEncoder().encode(
            {'message': "User created successfully"}
            ), 200
    else:
        return render_template('register.html', form=form)


@app.route('/users/<user_id>/edit', methods=['GET', 'POST'])
def update_user(user_id):
    user = User.find_by_id(user_id)
    form = UpdateUserForm()

    if request.method == 'PUT' and form.validate():
        data = {
            'full_name': request.form.get('full_name'),
            'username': request.form.get('username'),
            'bio': request.form.get('bio')
        }

        user.update(**data)
        return JSONEncoder.encode(
            {'message': "User updated successfully"}
            ), 200
    else:
        return render_template('update_user.html', user_id=user_id, form=form)


@app.route('/users/<user_id>', methods=['GET', 'DELETE'])
def user_operations(user_id):
    user_id = ObjectId(user_id)

    if request.method == "GET":
        user = User.find_by_id(user_id)
        if not user:
            return JSONEncoder().encode({'error': "User not found"}), 400
        return JSONEncoder().encode(user), 200
    elif request.method == "DELETE":
        users.find_one_and_delete({"_id": user_id})
        return JSONEncoder().encode(
            {'message': "User deleted successfully"}
            ), 200
    else:
        return JSONEncoder().encode({'error': "Method not allowed"}), 405


@app.route('/users', methods=['GET'])
def get_users():
    # Implement logic to retrieve user profile by username
    users = User.find_all_users()
    print(f"Users: {users}")
    return JSONEncoder().encode(users)
"""
