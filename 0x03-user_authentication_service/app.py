#!/usr/bin/env python3
"""a flask app """
from flask import Flask, jsonify, request, abort, redirect
from flask.wrappers import Response
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> Response:
    """a single get route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> Response:
    """ If the user does not exist, the end-point should register
        it and respond with the following JSON payload:
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": "<registered email>",
                       "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> Response:
    """login route"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({'email': email, 'message': 'logged in'})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> Response:
    """logout"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if session_id is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """implement a profile function to respond to the GET /profile route."""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if session_id is None or user is None:
        abort(403)
    return jsonify({"email": "<user email>"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
