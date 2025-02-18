#!/usr/bin/python3
"""
This is the module for the index view
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status/', methods=['GET'], strict_slashes=False)
def status():
    """returns app_views API status"""
    return jsonify(status='OK')


@app_views.route('/stats/', methods=['GET'], strict_slashes=False)
def stats():
    """This endpoint retrieves the number of each objects by type"""
    objects = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    response = {}
    for k, v in objects.items():
        response[v] = storage.count(k)

    return jsonify(response)
