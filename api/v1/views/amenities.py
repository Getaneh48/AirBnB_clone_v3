#!/usr/bin/python3
"""
Blueprint for amenities route
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """handles the method GET and POST for the route"""
    if request.method == 'GET':
        amenities = storage.all(Amenity)
        amenities_list = [amenity.to_dict() for key,
                          amenity in amenities.items()]
        return (jsonify(amenities_list))

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            if 'name' not in data:
                return (jsonify({'error': 'Missing name'})), 400

            amenity = Amenity(**data)
            amenity.save()
            return (jsonify(amenity.to_dict())), 201
        else:
            return (jsonify({'error': 'Not a JSON'})), 400


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'PUT'], strict_slashes=False)
def amenity(amenity_id):
    """handles the method GET and PUT for the route"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        if request.method == 'GET':
            return (jsonify(amenity.to_dict()))

        if request.method == 'DELETE':
            amenity.delete()
            amenity.save()
            return (jsonify({})), 200

        if request.method == 'PUT':
            data = request.get_json()
            amenity.name = data['name']
            amenity.save()
            return jsonify(amenity.to_dict()), 200
    else:
        abort(404)
