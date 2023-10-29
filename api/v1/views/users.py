#!/usr/bin/python3
"""This module is an RESTFul api for users object in the database
"""
from models import storage
from models.user import User
from flask import request, abort, jsonify
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """This function fetches all the users in the database
    """

    users = storage.all(User)

    user_list = []

    for user in users.values():
        user_list.append(user.to_dict())

    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """This function fetches an user, based on the id 'user_id', and
    raises a 404 error if the id is not linked to an user
    """

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """This function deletes an user, based on the given id 'user_id'
    if it mapped to an user. If not raises a 404 error
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """This function creates a new user and save it in the database
    """

    data = request.get_json()

    if not data:
        return jsonify('Not a JSON'), 400

    if 'email' not in data:
        return jsonify('Missing email'), 400
    elif 'password' not in data:
        return jsonify('Missing password'), 400

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """This function updates an existing user if the id 'user_id' is
    mapped to an user in the database, if not an error 404 is raised.
    The attributes id, created_at and updated_at are skipped if listed in
    The content sent with the request.
    """

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data = request.get_json()

    if data is None:
        return jsonify("Not a JSON"), 400

    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            # user.__dict__[key] = value
            # user.key = value
            setattr(user, key, value)
    # user.save()
    storage.save()

    return jsonify(user.to_dict()), 200
