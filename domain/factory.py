"""Defines classes for object creation."""

from domain.models.logic import ProtectedUser, SimpleUser, ObjectivesManager, TasksManager

class UserFactory:
    """Creates an instance of an user."""
    
    def create_user(self, user_name, password):
        """Instantiates an user class."""

        if password:
            return ProtectedUser(user_name, password)
        else:
            return SimpleUser(user_name) 
    

class ManagerFactory:
    """Creates an instance of an user."""
    
    def create(self, manager, db, user):
        """Instantiates the manager classes."""

        if manager == "objectives":
            return ObjectivesManager(db, user)
        elif manager == "tasks":
            return TasksManager(db, user)