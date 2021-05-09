#!/usr/bin/python3
""" Module on place view """
from api.v1.views import app_views
from models import storage
from models.amenity import Place
from flask import jsonify, request


@app_views.route('/places', methods=['GET'])
def places():
    """
        Function to return all place informations
    """
    places = storage.all(Place)
    obj = []
    for place, value in places.items():
        obj.append(value.to_dict())
    return(jsonify(obj))


@app_views.route('/places/<id_place>',
                 methods=['GET'], strict_slashes=False)
def place(id_place):
    """ return (JSON) """
    places = storage.all(Place)
    for place, value in places.items():
        if value.id == id_place:
            return jsonify(value.to_dict())
    return jsonify(error='Not found'), 404


@app_views.route('/places', methods=['POST'], strict_slashes=False)
def amenitie_post():
    """ Method post """
    content = request.get_json()
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    if 'name' in content:
        place = place(name=content['name'])
        place.save()
        return jsonify(place.to_dict()), 201
    return jsonify(error='Missing name'), 400


@app_views.route('/places/<id_place>',
                 methods=['PUT'], strict_slashes=False)
def amenitie_put(place_id):
    """ API Put methode """
    content = request.get_json()
    places = storage.all(Place)
    for place, value in places.items():
        if value.id == id_place:
            value.name = content['name']
            value.save()
            return jsonify(value.to_dict()), 200
    return jsonify(error='Not Found'), 404


@app_views.route('/places/<id_place>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(id_place):
    """ Function to return a place informations """
    places = storage.all(Place)
    for place, value in places.items():
        if value.id == id_place:
            storage.delete(value)
            storage.save()
            return jsonify({}), 200
    return jsonify(error='Not found'), 404
