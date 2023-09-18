"""Defines classes for object creation."""

from domain.models.logic import User

class UserFactory:
    """Creates an instance of an user."""
    
    def create_user(self, user_name):
        user = User(user_name)
        return user