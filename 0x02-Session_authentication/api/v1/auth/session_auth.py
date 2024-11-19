#!/usr/bin/env python3
""" a class for session authenticator"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """class SessionAuth that inherits from Auth"""
    user_id_by_session_id = {}

    def __init__(self):
        """initialization method"""

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id:"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID:"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a User instance based on a cookie value:"""
        if request is None:
            return None

        # Get the session ID from the cookie
        session_id = self.session_cookie(request)

        if session_id is None:
            return None

        # Get the user ID based on the session ID
        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return None

        # Retrieve and return the User instance from the database
        return User.get(user_id)
