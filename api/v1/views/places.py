#!/usr/bin/python3
""" Module on place view """
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from flask import jsonify, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """ Function to return all place informations """
    cities = storage.all(City)
    obj = []
    for city, value in cities.items():
        if value.id == city_id:
            for place in value.places:
                obj.append(place.to_dict())
                return jsonify(obj)
    return jsonify(error='Not found'), 404


@app_views.route('/places/<id_place>',
                 methods=['GET'], strict_slashes=False)
def place(id_place):
    """ return (JSON) """
    places = storage.all(Place)
    for place, value in places.items():
        if value.id == id_place:
            return jsonify(value.to_dict())
    return jsonify(error='Not found'), 404


@app_views.route('/places/<id_place>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(id_place):
    """ Function to return a place informations """
    places = storage.all(Place)
    for place, value in places.items():
        if value.id == id_place:
            storage.delete(value)
            storage.save()
            return jsonify({}), 200
    return jsonify(error='Not found'), 404


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """
        API POST
    """
    content = request.get_json()
    cities = storage.all(City)
    is_city = False
    for city, value in cities.items():
        if value.id == city_id:
            is_city = True
    if is_city is False:
        return jsonify(error="Not found"), 404
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    if 'name' not in content:
        return jsonify(error='Missing name'), 400
    if 'user_id' not in content:
        return jsonify(error='Missing user_id'), 400
    users = models.storage.all(User)
    is_user = False
    for user, value in users.items():
        if value.id == content['user_id']:
            is_user = True
    if is_user is False:
        return jsonify(error="Not found"), 404
    place = Place(name=content['name'], user_id=content['user_id'],
                  city_id=city_id)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<id_place>',
                 methods=['PUT'], strict_slashes=False)
def place_put(id_place):
    """ API Put methode """
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    content = request.get_json()
    places = storage.all(Place)
    for place, value in places.items():
        if value.id == id_place:
            value.name = content['name']
            value.save()
            return jsonify(value.to_dict()), 200
    return jsonify(error='Not Found'), 404
