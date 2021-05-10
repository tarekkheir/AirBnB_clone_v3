#!/usr/bin/python3
""" Module on state view """
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, request, abort, make_response


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def city(state_id):
    """ return (JSON) """
    states = storage.get(State, state_id)
    if states:
        obj = []
        for city in states.cities:
            obj.append(city.to_dict())
            return jsonify(obj)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities(city_id):
    """
        Function to return all cities informations
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def city_delete(city_id):
    """ Function to return a cities informations """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def city_post(state_id):
    """ Method post """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    body = request.get_json()
    body['state_id'] = state_id
    city = City(len(body), **body)
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_put(city_id):
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
