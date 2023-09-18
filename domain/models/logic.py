"""
Containts the classes that represent the core concepts of the
task management system.
"""

from abc import ABC, abstractmethod


class DataSource(ABC):
    """Ensures that the objects will receive the data."""
    @abstractmethod
    def get_user_data(self):
        pass


class DB(DataSource):
    """Deals with the user data."""
    
    def get_user_data(self, user):  
        """Extract the user data from the .txt file as a dictionary."""  
        try:
            with open(f'DB/{user.name}.txt', 'r') as file:
                file_data = file.read()
                return eval(file_data)
        except FileNotFoundError:
            return {'user_name': user.name, 'objectives': []}
        

    def save_user_data(self, user_data):
        """Save the user data in the .txt file."""

        with open(f'DB/{user_data["user_name"]}.txt', 'w') as file:
            file.write(str(user_data))


class User:
    """Defines the properties of the user."""

    def __init__(self, name):
        self.name = name

    
    def change_name(self, new_name, user_data):
        """Change the name of the user."""
        
        user_data['user_name'] = new_name
        
        return user_data
    

class Manager(ABC):
    """A contract for the managers."""

    def __init__(self, user_data):
        self.user_data = user_data

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def modify(self):
        pass


class ObjectivesManager(Manager):
    """Manages the objectives."""

    def __init__(self, user_data):
        super().__init__(user_data)


    def add(self, objective_title):
        """Save the objective to the user data."""

        for objectives in self.user_data['objectives']:
            if objectives['title'] == objective_title:
                return
            
        tmp_dict = {'title': objective_title, 'tasks': []}
        self.user_data['objectives'].append(tmp_dict)

        return self.user_data
    

    def delete(self, objective_num):
        """Deletes the objective from the user data."""

        del self.user_data['objectives'][int(objective_num) - 1]
        return self.user_data
    

    def modify(self, new_title, obj_num):
        """Modifies the objective's title."""
        self.user_data['objectives'][int(obj_num) - 1]['title'] = new_title



class TasksManager(Manager):
    """Manages the tasks."""

    def __init__(self, user_data):
        super().__init__(user_data)


    def add(self, task_title, due_date, obj_num):
        """Save the task to the objective list."""

        index = int(obj_num) - 1
        for task in self.user_data['objectives'][index]['tasks']:
            if task['title'] == task_title:
                return
            
        tmp_dict = {'title': task_title, 'due_date': due_date}
        self.user_data['objectives'][index]['tasks'].append(tmp_dict)

        return self.user_data
    

    def delete(self, task_num, obj_num):
        """Deletes the objective from the user data."""

        index_obj = int(obj_num) - 1
        index_tsk = int(task_num) - 1
        del self.user_data['objectives'][index_obj]['tasks'][index_tsk]
        return self.user_data
    

    def modify(self, new_title, new_dd, task_num, obj_num):
        """Modifies the objective's title."""

        index_obj = int(obj_num) - 1
        index_tsk = int(task_num) - 1
        self.user_data['objectives'][index_obj]['tasks'][index_tsk]['title'] = new_title
        self.user_data['objectives'][index_obj]['tasks'][index_tsk]['due_date'] = new_dd