#!/usr/bin/env python3
"""add an expiration date to a Session ID."""
from api.v1.auth.session_auth import SessionAuth
from datetime import timedelta, datetime
from os import getenv


class SessionExpAuth(SessionAuth):
    """session authentication with expiration"""

    def __init__(self):
        """initialize the session duration"""
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """overload create_session"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        # super can't create a session ID

        session_dictionary = {
                'user_id': user_id,
                'created_at': datetime.now()
            }

        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """overload"""
        if session_id is None:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None

        if self.session_duration <= 0:
            return session_dictionary.get('user_id')

        created_at = session_dictionary.get('created_at')
        if created_at is None:
            return None

        if created_at + timedelta(seconds=self.session_duration
                                  ) < datetime.now():
            return None
        return session_dictionary.get('user_id')
