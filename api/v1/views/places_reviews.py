#!/usr/bin/python3
""" Create a new view for Review object that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from models import storage
from models.reviews import Review
from models.place import Place


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def review_list(place_id):
    """ return (JSON) """
    places = storage.all(Place)
    rev = storage.all(Review)
    reviews = []

    for place in places.values():
        if place.id == place_id:
            for r in rev.values():
                if r.place_id == place_id:
                    reviews.append(r.to_dict())
            return jsonify(reviews)
    abort(404)



@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_all(review_id):
    """
        Function to return all cities informations
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return(jsonify(review.to_dict()))


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def review_delete(review_id):
    """ Function to return a cities informations """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def review_post(place_id):
    """ Method post """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.json:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'text' not in request.json:
        return make_response(jsonify({'error': 'Missing text'}), 400)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_put(city_id):
    """ API Put methode """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    body = request.get_json()

    body['name'] = city.name
    city.save()

    return jsonify(city.to_dict()), 200
