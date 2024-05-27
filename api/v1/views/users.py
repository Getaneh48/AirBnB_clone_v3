#!/usr/bin/python3
"""
Blueprint for user model route
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """
    handles http verb GET and POST to retrieve and create a
    user model
    """
    if request.method == 'GET':
        users = storage.all(User)
        users_list = [user.to_dict() for user in users.values()]
        return (jsonify(users_list))

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            if 'email' not in data:
                return (jsonify({'error': 'Missing name'})), 400

            if 'password' not in data:
                return (jsonify({'error': 'Missing name'})), 400

            user = User(**data)
            user.save()
            return (jsonify(user.to_dict())), 201
        else:
            return (jsonify({'error': 'Not a JSON'})), 400


@app_views.route('/users/<user_id>',
                 methods=['GET', 'PUT'], strict_slashes=False)
def user(user_id):
    """
    handles the http verb GET and PUT to retrieve and modify
    a specific user model
    """
    user = storage.get(User, user_id)
    if user:
        if request.method == 'GET':
            return (jsonify(user.to_dict()))

        if request.method == 'DELETE':
            user.delete()
            user.save()
            return (jsonify({})), 200

        if request.method == 'PUT':
            data = request.get_json()
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.password = data['password']
            user.save()
            return jsonify(user.to_dict()), 200
    else:
        abort(404)
