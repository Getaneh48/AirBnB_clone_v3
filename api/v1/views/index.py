#!/usr/bin/python3
"""
Blueprint for the status route
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """
        returns a JSON: "status": "OK"
    """
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def count_objects():
    """
         retrieves the count of each models
    """
    cls_counts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(cls_counts)
