#!/usr/bin/env python3
"""define a _hash_password method that takes in a
password string arguments and returns bytes."""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """define a _hash_password method that takes in a
        password string arguments and returns bytes.
    """
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


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
