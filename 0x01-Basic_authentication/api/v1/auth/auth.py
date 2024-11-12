#!/usr/bin/env python3
""" the authenticator class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ The Auth"""
    def __init__(self):
        """the initialization method"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ public method"""
        return False

    def authorization_header(self, request=None) -> str:
        """public method"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """public method"""
        return None
