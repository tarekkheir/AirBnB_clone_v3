#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
import json
import models
from models import storage
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """
        return (JSON)
        a dict with status and ok
    """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'])
def stats():
    """
        Function to return the number of all object
    """
    obj = {
        "amenities": models.storage.count(Amenity),
        "cities": models.storage.count(City),
        "places": models.storage.count(Place),
        "reviews": models.storage.count(Review),
        "states": models.storage.count(State),
        "users": models.storage.count(User)
    }
    return jsonify(obj)
