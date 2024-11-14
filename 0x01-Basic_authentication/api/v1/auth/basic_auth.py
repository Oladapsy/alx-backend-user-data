#!/usr/bin/env python3
""" Basic authentication class"""
from .auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ BasicAuth that inherits from Auth"""
    def __init__(self):
        """initialization"""

    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        """ returns the Base64 part of the Authorization
            header for a Basic Authentication:
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ returns the decoded value of a Base64
            string base64_authorization_header:
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decode_byte = base64.b64decode(base64_authorization_header)
            return decode_byte.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """BasicAuth that returns the user email and password from
            the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        split = decoded_base64_authorization_header.split(":", 1)
        return (split[0], split[1])

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """returns the User instance based on his email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search(attributes={'email': user_email})
        except Exception:
            return None
        if not user:
            return None
        # Get the first user from the search results
        user = user[0]
        # Return None if the password is invalid
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request:"""
        # check if the request contain header
        # authorization header is gotten from the Auth class
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None

        # Step 2: Extract base64 part from the authorization header
        base64_authorization = self.extract_base64_authorization_header(auth_header)  # noqa
        if not base64_authorization:
            return None

        # Step 3: Decode base64 authorization to get "email:password" format
        decoded_auth = self.decode_base64_authorization_header(base64_authorization)  # noqa
        if not decoded_auth:
            return None

        # Step 4: Extract email and password from decoded credentials
        email, password = self.extract_user_credentials(decoded_auth)
        if not email or not password:
            return None

        # Step 5: Get the User instance based on email and password
        user = self.user_object_from_credentials(email, password)
        return user  # return
