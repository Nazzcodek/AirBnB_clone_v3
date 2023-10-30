#!/usr/bin/python3
"""
This is the module for the Place view
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'],
                 strict_slashes=False
                 )
def places_by_city(city_id):
    """This method retrive and create place(s) in a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404, 'Not found')

    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return jsonify(places)

    if request.method == 'POST':
        data = request.get_json()

        if not data:
            abort(400, 'Not a JSON')

        if 'user_id' not in data:
            abort(400, 'Missing user_id')

        user = storage.get(User, data['user_id'])
        if not user:
            abort(404)

        if 'name' not in data:
            return abort(400, 'Missing name')
        data['city_id'] = city_id
        place = Place(**data)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>/',
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def modify_place(place_id):
    """This method modifies the place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify(), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        attr = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for k, v in data.items():
            if k not in attr:
                setattr(place, k, v)
        storage.save()
        return jsonify(place.to_dict()), 200


@app_views.route('/places_search/', methods=['POST'], strict_slashes=False)
def search_place():
    """
    This endpoint retrieves all Place objects
    depending of the JSON in the body of the request.
    """
    places = [place for place in storage.all('Place').values()]

    # get json data
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    # extract parameter if exist and set to empty if not exist
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    # fiter by states and cities
    if states:
        cities = storage.all(City)
        state_cities = set([city.id for city in cities.values()
                            if city.state_id in states])
    else:
        state_cities = set()

    # get all specified cities
    if cities:
        cities = set(
            [city_id for city_id in cities if storage.get(City, city_id)])
        state_cities = state_cities.union(cities)

    # Filter places based on specified cities
    if state_cities:
        places = [place for place in places if place.city_id in state_cities]

    # Return all places if no amenities are specified
    elif amenities is None:
        place_dict = [place.to_dict() for place in places]
        return jsonify(place_dict)

    # Filter places based on specified amenities
    places_amenities = []
    if amenities:
        amenities = set([amenity_id for amenity_id in amenities
                         if storage.get(Amenity, amenity_id)])
        for place in places:
            place_amenities = None
            if STORAGE_TYPE == 'db' and place.amenities:
                place_amenities = [amenity.id for amenity in place.amenities]
            elif place.amenities:
                place_amenities = place.amenities
            amenity = all(
                [amenity in place_amenities for amenity in amenities])
            if place_amenities and amenity:
                places_amenities.append(place)

    else:
        places_amenities = places

    # filter place
    place_dict = [place.to_dict() for place in places_amenities]
    return jsonify(place_dict)
