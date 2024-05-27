#!/usr/bin/python3
"""
Blueprint for places model route
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def all_city_places(city_id):
    """
    handles the http verb GET and POST to retrieve and create
    places for a given city
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return (jsonify(places))

    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
                if 'user_id' not in data:
                    return jsonify({'error', 'Missing user_id'}), 400
                user = storage.get(User, data['user_id'])
                if not user:
                    abort(404)
                if 'name' not in data:
                    return jsonify({'error': 'Missing name'}), 400

                data['city_id'] = city_id
                place = Place(**data)
                place.save()

                return (jsonify(place.to_dict())), 201
            else:
                return (jsonify({'error': 'Not a JSON'})), 400
        except TypeError:
            abort(500)


@app_views.route('/places/<place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def place(place_id):
    """
    handles the http verb GET, PUT and DELETE to get, modify and delete
    a specific place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        return (jsonify(place.to_dict()))

    if request.method == 'DELETE':
        place.delete()
        place.save()
        return (jsonify({})), 200

    if request.method == 'PUT':
        try:
            data = request.get_json()
            if request.is_json:
                place.name = data['name']
                place.description = data['description']
                place.save()
                return (jsonify(place.to_dict())), 200
            else:
                return (jsonify({'error': 'Not a JSON'})), 400
        except Exception:
            return (jsonify({'error': 'Not a JSON'})), 400
