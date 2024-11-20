#!/usr/bin/env python3
"""define a _hash_password method that takes in a
password string arguments and returns bytes."""
import bcrypt


def _hash_password(password: str) -> str:
    """define a _hash_password method that takes in a
        password string arguments and returns bytes.
    """
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
