#!/usr/bin/env python3
""" the authenticator class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ The Auth"""
    def __init__(self):
        """the initialization method"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns True if the path is not in the
            list of strings excluded_paths:
        """
        if path is None:
            return True
        ex_len = len(excluded_paths)
        if excluded_paths is None or ex_len == 0:
            return True

        normalize_path = path.rstrip('/')
        for excluded in excluded_paths:
            normalize_excluded = excluded.rstrip("/")
            if normalize_path == normalize_excluded:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """public method"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """public method"""
        return None
