#!/usr/bin/python3
"""This is the module for place review API"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('places/<place_id>/reviews/',
                 methods=['GET', 'POST'],
                 strict_slashes=False
                 )
def place_reviews(place_id):
    """this method retrieves and create reviews from place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)

    if request.method == 'POST':
        data = request.get_json()

        if not data:
            abort(400, 'Not a JSON')

        if 'user_id' not in data:
            abort(400, 'Missing user_id')

        user = storage.get(User, data['user_id'])

        if not user:
            abort(404)

        if 'text' not in data:
            return abort(400, 'Missing text')

        data['place_id'] = place_id
        review = Review(**data)
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route('reviews/<review_id>/',
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False
                 )
def modify_reviews(review_id):
    """This method modifies the places review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify(), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        attr = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for k, v in data.items():
            if k not in attr:
                setattr(review, k, v)
        storage.save()
        return jsonify(review.to_dict()), 200
