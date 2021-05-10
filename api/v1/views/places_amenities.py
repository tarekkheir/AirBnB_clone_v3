#!/usr/bin/python3
""" Place Amenities """
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from models import storage
from models.review import Review
from models.user import User
from models.amenity import Amenity
from models.place import Place
import os


@app_views.route(
    '/places/<place_id>/amenities',
    methods=['GET'],
    strict_slashes=False)
def place_amenities(place_id):
    """ get amenities """
    places = storage.all(Place)
    obj = []
    for place, value in places.items():
        if value.id == place_id:
            if os.getenv('HBNB_TYPE_STORAGE') == "db":
                for amenitie, value2 in value.amenities.items:
                    obj.append(value2.to_dict())
                return (jsonify(obj))
            else:
                return (jsonify(value.amenity_ids))
    return jsonify(error='Not found'), 404
