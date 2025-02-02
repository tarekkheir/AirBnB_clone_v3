#!/usr/bin/python3
""" new view for User object that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request, make_response
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def users_list():
    """ Retrieves the list of all User objects"""
    users = storage.all(User)
    obj = []

    for user, value in users.items():
        obj.append(value.to_dict())

    return jsonify(obj)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_obj(user_id):
    """ Retrieves a User object"""
    users = storage.get(User, user_id)

    if users is None:
        abort(404)
    return jsonify(users.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def user_delete(user_id):
    """ Deletes a User object"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_create():
    """ Creates a User"""
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.json:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.json:
        return make_response(jsonify({'error': 'Missing password'}), 400)

    body = request.get_json()
    user = User(len(body), **body)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_put(user_id):
    """ Updates a User object"""
    user = storage.get(user, user_id)

    if user is None:
        abort(404)

    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    body = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in body.items():
        if key not in ignore_keys:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
