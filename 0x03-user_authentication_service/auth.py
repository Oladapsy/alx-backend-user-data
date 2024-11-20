#!/usr/bin/env python3
"""define a _hash_password method that takes in a
password string arguments and returns bytes."""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> str:
    """define a _hash_password method that takes in a
        password string arguments and returns bytes.
    """
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """takes password and email and return User obj"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exist")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Try locating the user by email. If it exists,
            check the password with bcrypt.checkpw.
            If it matches return True. In any other case, return False
        """
        try:
            user = self._db.find_user_by(email=email)
            u_passwd = user.hashed_password
            return bcrypt.checkpw(password.encode('utf-8'), u_passwd)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """returns session_id as a string"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """It takes a single session_id string argument and returns
        the corresponding User or None.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
