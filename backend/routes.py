import json

from flask import jsonify, request
from bson import ObjectId
from app import app
from models import User, RegistrationForm

# ... import other necessary modules like Flask-Security

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
def create_user():
    user_data = request.get_json()
    form = RegistrationForm(data=user_data)

    if form.validate():
        new_user = User(**user_data)
        new_user.save()
        return JSONEncoder().encode({'message': "User created successfully"})
    else:
        errors = form.errors
        return jsonify({'errrors': errors}), 400

@app.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_operations(user_id):
    user_id = ObjectId(user_id)

    if request.method == "GET":
        user = User.find_by_id(user_id)
        if not user:
            return JSONEncoder().encode({'error': "User not found"})
        return JSONEncoder().encode(user)
    elif request.method == "PUT":
        user_data = request.get_json()
        users.find_one_and_update({"_id": user_id}, {"$set": user_data})
        return JSONEncoder().encode({'message': "User updated successfully"})
    elif request.method == "DELETE":
        users.find_one_and_delete({"_id": user_id})
        return JSONEncoder().encode({'message': "User deleted successfully"})
    else:
        return JSONEncoder().encode({'error': "Method not allowed"}), 405

@app.route('/users', methods=['GET'])
def get_users():
    # Implement logic to retrieve user profile by username
    users = User.find_all_users()
    print(f"Users: {users}")
    return JSONEncoder().encode(users)