#!/usr/bin/python3
"""
Blueprint for review model route
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from models.city import City


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def place_reviews(place_id):
    """handles a GET and POST verbs for reviews of a specific place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return (jsonify(reviews))

    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
                if 'user_id' not in data:
                    return make_response({'error', 'Missing user_id'}, 400)
                user = storage.get(User, data['user_id'])
                if not user:
                    abort(404)
                if 'text' not in data:
                    return jsonify({'error': 'Missing text'}), 400

                data['place_id'] = place_id
                review = Review(**data)
                review.save()

                return (jsonify(review.to_dict())), 201
            else:
                return (jsonify({'error': 'Not a JSON'})), 400
        except TypeError:
            abort(500)


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def review(review_id):
    """handles a GET, PUT and DELETE verbs of a review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if request.method == 'GET':
        return (jsonify(review.to_dict()))

    if request.method == 'DELETE':
        review.delete()
        review.save()
        return (jsonify({})), 200

    if request.method == 'PUT':
        data = request.get_json()
        if request.is_json:
            review.text = data['text']
            review.save()
            return (jsonify(review.to_dict())), 200
        else:
            return (jsonify({'error': 'Not a JSON'})), 400
