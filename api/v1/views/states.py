#!/usr/bin/python3
"""
Blue print for state model routes
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states",
                 methods=['GET', 'POST'], strict_slashes=False)
def states():
    """
    returns all states objects in json format
    """
    if request.method == 'GET':
        all_states = storage.all(State)
        state_dict = []
        for key, value in all_states.items():
            state_dict.append(value.to_dict())

        return (jsonify(state_dict))

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            if 'name' not in data:
                return jsonify({"error": "Missing Name"}), 400

            state = State(**data)
            state.save()
            return (jsonify(state.to_dict())), 201
        else:
            return jsonify({'error': 'Not a JSON'}), 400

        return ""


@app_views.route("/states/<state_id>", methods=['GET', 'DELETE', 'PUT'])
def state_by_id(state_id):
    """
    handles the http verb GET, DELETE and PUT to retrieve, delete, and
    modifiy a state
    """
    if request.method == 'GET':
        try:
            state = storage.get(State, state_id)
            return (jsonify(state.to_dict()))
        except Exception:
            abort(404)

    if request.method == 'DELETE':
        state = storage.get(State, state_id)
        if state:
            state.delete()
            storage.save()
            return (jsonify({})), 200
        else:
            abort(404)

    if request.method == 'PUT':
        if request.is_json:
            data = request.get_json()
            state = storage.get(State, state_id)
            if state is None:
                abort(404)

            state.name = data['name']
            state.save()
            return jsonify(state.to_dict()), 200
        else:
            abort(404)
