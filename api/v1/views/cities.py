#!/usr/bin/python3
"""
This module implements a city api
"""
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """This method fetches the cities attached to a state
    in database
    """

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())

    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """This function retrieves a city based on the city ID.
    if the id 'city_id' is not mapped to a city, a 404 error is raised
    """

    city = storage.get(City, city_id)

    # When the city is not in the database
    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """This function deletes a city in the database, if the id 'city_id'
    is mapped to a city. Otherwise a 404 state_code is returned
    """

    city = storage.get(City, city_id)

    # When the city is not in the database
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """This function creates a new city. If the id 'state_id' is not mapped
    to a state, a 404 error status code is sent as the response to the request.
    A 400 error status code is sent as the response to the request, if the
    content type is not JSON'ed or if the content has no name attribute.
    """

    state = storage.get(State, state_id)

    # When the state is not in the database
    if state is None:
        abort(404)

    data = request.get_json()
    print("\n\n\n==============Got Here==================\n\n\n")

    if not data:
        # print('\n\n\n=====\nSent the Error Message for not JSON.\n=====\n\n')
        return jsonify("Not a JSON"), 400
    if 'name' not in data:
        # print('\n\n\n======\nSent the Error Message for no name.\n======\n\n')
        return jsonify("Missing name"), 400
        # abort(400, "Missing name")

    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """This function updates a city in the database, only the city id 'city_id'
    is mapped to a city, otherwise a 404 error is sent as the response.
    This error response is also for inaccurate content type.
    """

    state = storage.get(City, city_id)

    if state is None:
        abort(404)

    data = request.get_json()

    if not data:
        return jsonify('Not a JSON'), 400

    for key, value in data.items():
        if key in ['id', 'state_id', 'created_at', 'updated_at']:
            pass
        else:
            state.__dict__[key] = value
    storage.save()
    return jsonify(state.to_dict()), 200
