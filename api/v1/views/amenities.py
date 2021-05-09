#!/usr/bin/python3
""" Module on amenitie view """
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, request


@app_views.route('/amenities', methods=['GET'])
def amenities():
    """
        Function to return all amenitie informations
    """
    amenities = storage.all(amenitie)
    obj = []
    for amenitie, value in amenities.items():
        obj.append(value.to_dict())
    return(jsonify(obj))


@app_views.route('/amenities/<id_amenitie>', methods=['GET'], strict_slashes=False)
def amenitie(id_amenitie):
    """ return (JSON) """
    amenities = storage.all(amenitie)
    for amenitie, value in amenities.items():
        if value.id == id_amenitie:
            return jsonify(value.to_dict())
    return jsonify(error='Not found'), 404


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenitie_post():
    """ Method post """
    content = request.get_json()
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    if 'name' in content:
        amenitie = amenitie(name=content['name'])
        amenitie.save()
        return jsonify(amenitie.to_dict()), 201
    return jsonify(error='Missing name'), 400


@app_views.route('/amenities/<amenitie_id>', methods=['PUT'], strict_slashes=False)
def amenitie_put(amenitie_id):
    """ API Put methode """
    content = request.get_json()
    amenities = storage.all(amenitie)
    for amenitie, value in amenities.items():
        if value.id == amenitie_id:
            value.name = content['name']
            value.save()
            return jsonify(value.to_dict()), 200
    return jsonify(error='Not Found'), 404

@app_views.route('/amenities/<id_amenitie>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(id_amenitie):
    """ Function to return a amenitie informations """
    amenities = storage.all(amenitie)
    for amenitie, value in amenities.items():
        if value.id == id_amenitie:
            storage.delete(value)
            storage.save()
            return jsonify({}), 200
    return jsonify(error='Not found'), 404