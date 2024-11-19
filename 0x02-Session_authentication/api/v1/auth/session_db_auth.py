#!/usr/bin/env python3
""" Session database authentication """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session authentication with database storage """

    def create_session(self, user_id=None):
        """ Create a new session and store it in the database """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve user ID by session ID """
        if session_id is None:
            return None

        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return None

        session = sessions[0]
        if self.session_duration <= 0:
            return session.user_id

        created_at = session.created_at
        if created_at is None:
            return None

        if created_at + timedelta(seconds=self.session_duration
                                  ) < datetime.now():
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """ Destroy a session based on the request cookie """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return False

        session = sessions[0]
        session.remove()
        return True
