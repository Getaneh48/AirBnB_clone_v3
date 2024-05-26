#!/usr/bin/python3
"""
Blueprint for cities route
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'], strict_slashes=False)
def state_cities(state_id):
    state  = storage.get(State, state_id)
    
    if state:
        if request.method == 'GET':
            cities = [ city.to_dict() for city in state.cities]
            return (jsonify(cities))

        if request.method == 'POST':
            data = request.get_json()

            if request.is_json:
                if 'name' not in data:
                    return make_response(jsonify({"error":"Missing Name"}), 400)

                data['state_id'] = state_id
                city = City(**data)
                city.save()
                return jsonify(city.to_dict()), 201
            else:
                return make_response(jsonify({"error":"Not a JSON"}), 400)

    else:
        abort(404)

@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def cities(city_id):
    city = storage.get(City, city_id)
    if city:
        if request.method == 'GET':
            return (jsonify(city.to_dict()))

        if request.method == 'DELETE':
            city.delete()
            city.save()
            return (jsonify({})), 200

        if request.method == 'PUT':
            data = request.get_json()
            city.name = data['name']
            city.save()
            return jsonify(city.to_dict()), 200
    else:
        abort(404)
