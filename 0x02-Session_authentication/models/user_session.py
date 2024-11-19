#!/usr/bin/env python3
"""user section class"""
from models.base import Base


class UserSession(Base):
    """a userv session class"""
    def __init__(self, *args: list, **kwargs: dict):
        """ initialization"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
