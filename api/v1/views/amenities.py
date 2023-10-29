#!/usr/bin/python3
"""This module is an RESTFul api for amenities object in the database
"""
from models import storage
from models.amenity import Amenity
from flask import request, abort, jsonify
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """This function fetches all the amenities in the database
    """

    amenities = storage.all(Amenity)

    amen_list = []

    for amenity in amenities.values():
        amen_list.append(amenity.to_dict())

    return jsonify(amen_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """This function fetches an amenity, based on the id 'amenity_id', and
    raises a 404 error if the id is not linked to an amenity
    """

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """This function deletes an amenity, based on the given id 'amenity_id'
    if it mapped to an amentiy. If not raises a 404 error
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """This function creates a new amenity and save it in the database
    """

    data = request.get_json()

    if not data:
        return jsonify('Not a JSON'), 400

    if 'name' not in data:
        return jsonify('Missing name'), 400

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """This function updates an existing amenity if the id 'amenity_id' is
    mapped to an amenity in the database, if not an error 404 is raised.
    The attributes id, created_at and updated_at are skipped if listed in
    The content sent with the request.
    """

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify("Not a JSON"), 400

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            amenity.__dict__[key] = value

    amenity.save()
    # storage.save()
    return jsonify(amenity.to_dict()), 200
