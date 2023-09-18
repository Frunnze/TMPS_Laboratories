"""Classes for dealing with UI."""

from abc import ABC, abstractmethod


class LoginUI:
    """Deals with the registration into the system."""

    def login(self):
        """Asks for the user login."""

        print('\n'*50 + 'Welcome to the Task Management System!')
        login = input('Login: ')
        return login
    

class Lists(ABC):
    
    def __init__(self, user_data):
        self.user_data = user_data

    @abstractmethod
    def display_list(self):
        pass
    

class ObjectivesUIList(Lists):
    """Represents the list with the objectives."""

    def __init__(self, user_data):
        self.user_data = user_data
        self.width = 49


    def display_list(self):
        """Lists all the objectives that you have."""

        print('-'*self.width + '\n'*50)
        print('User: ' + self.user_data['user_name'])
        print('-'*self.width)
        print('Objectives: ')
        print('-'*self.width)

        if self.user_data['objectives']:
            num = 0
            for objective in self.user_data['objectives']:
                num += 1 
                print(str(num) + ' - ' + objective['title'])
        else:
            print(' '*4 + 'No objectives.')


class TasksUIList(Lists):
    """Displays the list of tasks."""

    def __init__(self, user_data):
        super().__init__(user_data)
        self.width = 49


    def display_list(self, obj_num):
        """Lists all the tasks that you have in the objective."""

        index = int(obj_num)-1
        print('-'*self.width + '\n'*50)
        print('User: ' + self.user_data['user_name'])
        print('-'*self.width)
        print('Objective: ' + self.user_data['objectives'][index]['title'])
        print('Tasks: ')
        print('-'*self.width)

        if self.user_data['objectives'][index]['tasks']:
            num = 0
            for task in self.user_data['objectives'][index]['tasks']:
                num += 1 
                print(str(num) + ' - ' + task['title'] + ' - ' + task['due_date'])
        else:
            print(' '*4 + 'No tasks.')


class Commands(ABC):

    @abstractmethod
    def display_commands(self):
        pass


class ObjectivesUIBasicCommands(Commands):
        
        def __init__(self):
            self.width = 49

        def display_commands(self):
            """Gives a list of commands to apply on the objectives."""
            
            print('-'*self.width)
            print('< back | + add | - delete | o - open | m - modify')
            print('-'*self.width)


class TasksUIBasicCommands(Commands):
        
        def __init__(self):
            self.width = 49

        def display_commands(self):
            """Gives a list of commands to apply on the tasks."""
            
            print('-'*self.width)
            print('< back | + add | - delete | m - modify')
            print('-'*self.width)


class TasksUIOptionalCommands(TasksUIBasicCommands):
        """For LSP."""
        
        def __init__(self):
            super().__init__()

        def display_optional_task_commands(self):
            """Gives a list of optional commands to apply on the tasks."""
            
            print('-'*self.width)
            print('X - delete every task')
            print('-'*self.width)