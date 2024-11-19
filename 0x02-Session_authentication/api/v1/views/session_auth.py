#!/usr/bin/env python3
"""Session authentication views route"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """login rouute"""
    u_email = request.form.get(email)
    if not u_email:
        return jsonify({"error": "email missing"}), 400

    u_password = request.form.get(password)
    if not u_password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': u_email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    for u in user:
        if u.is_valid_password(u_password):
            from api.v1.app import auth
            session_id = auth.create_session(u.id)
            user_json = jsonify(u.to_json())
            user_json.set_cookie(getenv('SESSION_NAME'), session_id)
            return user_json
        else:
            return jsonify({"error": "wrong password"}), 401
