#!/usr/bin/python3
""" new view for User object that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def users_list():
    users = storage.all(User)
    obj = []

    for user in users.items():
        obj.append(user)

    return jsonify(obj.to_dict)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_obj(user_id):
    users = storage.get(User, user_id)

    if users is None:
        abort(404)

    return jsonify(users.to_dict)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def user_delete(user_id):
    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_create():
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.json:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.json:
        return make_response(jsonify({'error': 'Missing password'}), 400)

    body = request.get_json()
    user = User(len(body), **body)
    user.save()

    return jsonify(user.to_dict), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_put(user_id):
    user = storage.get(user, user_id)

    if user is None:
        abort(404)

    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    body = request.get_json()
    body['email'] = user.email
    body['password'] = user.password
    user.save()

    return jsonify(user.to_dict()), 200
