#!/usr/bin/python3
"""This module implements a API for the places-review relationship
for the place and review object of the airbnb clone.
"""

from models import storage
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from flask import request, abort, jsonify
from os import getenv


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """This fucntion retrieves the amenities of a place.
    However if the given place id 'place_id' is not
    mapped to a place, a 404 error is raised.
    """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity_list = []

    # For the database storage
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        for amenity in place.amenities:
            amenity_list.append(amenity.to_dict())

        return jsonify(amenity_list)

    # For file storage
    for amenity in place.amenities():
        amenity_list.append(amenity.to_dict())

    return jsonify(amenity_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """This function deletes an amenity mapped to a place, otherwise
    if the place id 'place_id' or amenity id 'amenity_id' is not linked
    a 404 error is raised
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        for amenity in place.amenities:
            if amenity_id == amenity.id:
                storage.delete(amenity)
                storage.save()
                return jsonify({}), 200

        # After looping if the amenity id is not linked to the place
        abort(404)

    # for the file storage
    for amenity in place.amenities():
        if amenity_id == amenity.id:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200

    # After looping if the amenity id is not linked to the place
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def update_place_amenity(place_id, amenity_id):
    """This function update's a place's list of amenities
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        for amenity in place.amenities:
            if amenity_id == amenity.id:
                return jsonify(amenity.to_dict()), 200

        # After looping if the amenity id is not linked to the place
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201

    # for the file storage
    for amenity in place.amenities():
        if amenity_id == amenity.id:
            return jsonify(amenity.to_dict()), 200

    # After looping if the amenity id is not linked to the place
    place.amenity_id.append(amenity_id)
    amenity.save()
    return jsonify(amenity.to_dict()), 201
