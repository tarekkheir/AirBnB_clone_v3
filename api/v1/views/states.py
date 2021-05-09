#!/usr/bin/python3
""" Module on state view """
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, request


@app_views.route('/states', methods=['GET'])
def states():
    """
        Function to return all state informations
    """
    states = storage.all(State)
    obj = []
    for state, value in states.items():
        obj.append(value.to_dict())
    return(jsonify(obj))


@app_views.route('/states/<id_state>', methods=['GET'], strict_slashes=False)
def state(id_state):
    """ return (JSON) """
    states = storage.all(State)
    for state, value in states.items():
        if value.id == id_state:
            return jsonify(value.to_dict())
    return jsonify(error='Not found'), 404


@app_views.route('/states/<id_state>',
                 methods=['DELETE'], strict_slashes=False)
def delete(id_state):
    """ Function to return a state informations """
    states = storage.all(State)
    for state, value in states.items():
        if value.id == id_state:
            storage.delete(value)
            storage.save()
            return jsonify({}), 200
    return jsonify(error='Not found'), 404


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """ Method post """
    content = request.get_json()
    if request.is_json is False:
        return jsonify(error='Not a JSON'), 400
    if 'name' in content:
        state = State(name=content['name'])
        state.save()
        return jsonify(state.to_dict()), 201
    return jsonify(error='Missing name'), 400


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_put(state_id):
    """ API Put methode """
    content = request.get_json()
    states = storage.all(State)
    for state, value in states.items():
        if value.id == state_id:
            value.name = content['name']
            value.save()
            return jsonify(value.to_dict()), 200
    return jsonify(error='Not Found'), 404
