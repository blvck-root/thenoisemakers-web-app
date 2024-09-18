import json

from flask import jsonify, request
from bson import ObjectId
from app import app, csrf
from models.user import User, RegistrationForm, UpdateUserForm

users = User.collection


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


# implement logic to display home page
@app.route('/')
def hello_noisemakers():
    # render home template
    return "<p>Hello, Noisemakers!</p>"


@app.route('/users', methods=['POST'])
@csrf.exempt
def create_user():
    user_data = request.get_json()
    form = RegistrationForm(data=user_data)

    if form.validate():
        new_user = User(**user_data)
        new_user.save()
        return JSONEncoder().encode(
            {'message': "User created successfully"}
            ), 200
    else:
        errors = form.errors
        return jsonify({'errors': errors}), 400


@app.route('/users/<user_id>', methods=['PUT'])
@csrf.exempt
def update_user(user_id):
    user = User.find_by_id(user_id)
    user_data = request.get_json()
    form = UpdateUserForm()

    if form.validate():
        try:
            user.update(**user_data)
            return JSONEncoder.encode(
                {'message': "User updated successfully"}
                ), 200
        except ValueError as e:
            return JSONEncoder.encode({'error': e}), 400
    else:
        errors = form.errors
        return jsonify({'errors': errors}), 400

@app.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
@csrf.exempt
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
    """
        elif request.method == "PUT":
        user_data = request.get_json()
        users.find_one_and_update({"_id": user_id}, {"$set": user_data})
        return JSONEncoder().encode({'message': "User updated successfully"})
    """


@app.route('/users', methods=['GET'])
def get_users():
    # Implement logic to retrieve user profile by username
    users = User.find_all_users()
    print(f"Users: {users}")
    return JSONEncoder().encode(users)
