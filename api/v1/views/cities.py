#!/usr/bin/python3
""" Module on state view """
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, request



@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def city(state_id):
    """ return (JSON) """
    states = storage.all(State)
    obj = []
    for city, value in state.cities.items():
        obj.append(value.to_dict())
        return jsonify(obj)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities(city_id):
    """
        Function to return all cities informations
    """
    cities = storage.all(City)
    for city, value in cities.items():
        if value.id == city_id:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete(city_id):
    """ Function to return a cities informations """
    cities = storage.all(City)
    for city, value in cities.items():
        if value.id == city_id:
            storage.delete(value)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def city_post():
    """ Method post """
    content = request.get_json()
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    
    state = State(name=content['name'])
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_put(city_id):
    """ API Put methode """
    content = request.get_json()
    cities = storage.all(City)

    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for cities, value in cities.items():
        if value.id == city_id:
            value.name = content['name']
            value.save()
            return jsonify(value.to_dict()), 200
