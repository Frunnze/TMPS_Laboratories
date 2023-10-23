"""Classes for dealing with UI."""

from abc import ABC, abstractmethod
from domain.models.logic import SingletonMeta


class Page:

    def __init__(self):
        self.header = None
        self.body = None
        self.footer = None

    def display_page(self, user_data):
        self.header.user_data = user_data
        self.header.display()
        self.body.user_data = user_data
        self.body.display_list()
        self.footer.display_commands()


class PageBuilder(ABC):

    @abstractmethod
    def create_header(self):
        pass

    @abstractmethod
    def create_body(self):
        pass

    @abstractmethod
    def create_footer(self):
        pass

    @abstractmethod
    def get_page(self):
        pass


class ObjectivesPageBuilder(PageBuilder):

    def __init__(self, header, objectives, commands):
        self.product = Page()
        self.header = header
        self.objectives = objectives
        self.commands = commands

    def create_header(self):
        self.product.header = self.header

    def create_body(self):
        self.product.body = self.objectives

    def create_footer(self):
        self.product.footer = self.commands

    def get_page(self):
        return self.product


class TasksPageBuilder(PageBuilder):

    def __init__(self, header, tasks, commands):
        self.product = Page()
        self.header = header
        self.tasks = tasks
        self.commands = commands

    def create_header(self):
        self.product.header =  self.header

    def create_body(self):
        self.product.body = self.tasks

    def create_footer(self):
        self.product.footer = self.commands

    def get_page(self):
        return self.product


class LoginUI(metaclass=SingletonMeta):
    """Deals with the registration into the system."""

    def login(self):
        """Asks for the user login."""

        print('\n'*50 + 'Welcome to the Task Management System!')
        login = input('Login: ')
        password = input('Password: ')
        if password == '-' or password == '': 
            password = None

        return login, password
    

class Lists(ABC):
    
    def __init__(self, user_data):
        self.user_data = user_data

    @abstractmethod
    def display_list(self):
        pass
    

class Header:
    def __init__(self, user_data):
        self.user_data = user_data
        self.width = 49
        self.jump = 50

    def display(self):
        print('-'*self.width + '\n'*self.jump)
        print('User: ' + self.user_data['user_name'])


class HeaderDecorator:
    def __init__(self, header, password):
        self.width = 49
        self.header = header
        self.password = password
        self.user_data = None

    def display(self):
        print('\n'*50)
        if self.password:
            print('Protected')
        else:
            print('Unprotected')
        
        self.header.user_data = self.user_data
        self.header.jump = 0
        self.header.display()


class ObjectivesUIList(Lists):
    """Represents the list with the objectives."""

    def __init__(self, user_data):
        self.user_data = user_data
        self.width = 49


    def display_list(self):
        """Lists all the objectives that you have."""

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
        self.obj_num = None


    def display_list(self):
        """Lists all the tasks that you have in the objective."""

        index = int(self.obj_num)-1
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

    @abstractmethod
    def clone(self):
        pass


class ObjectivesUIBasicCommands(Commands):
        
    def __init__(self):
        self.width = 49

    def display_commands(self):
        """Gives a list of commands to apply on the objectives."""
        
        print('-'*self.width)
        print('< back | + add | - delete | o - open | m - modify')
        print('-'*self.width)

    def clone(self):
        """Clone it in case there will be layers where you need these
        exact options."""

        obj = ObjectivesUIBasicCommands()
        obj.width = self.width
        return obj


class TasksUIBasicCommands(Commands):
        
    def __init__(self):
        self.width = 49

    def display_commands(self):
        """Gives a list of commands to apply on the tasks."""
        
        print('-'*self.width)
        print('< back | + add | - delete | m - modify')
        print('-'*self.width)
    
    def clone(self):
        """Clone it in case there will be layers where you need these
        exact options."""

        obj = TasksUIBasicCommands()
        obj.width = self.width
        return obj
        

class TasksUICommandsDecorator:
    def __init__(self, basic_commands_object):
        self.width = 49
        self.basic_commands_object = basic_commands_object

    def display_commands(self):
        """Gives a list of commands to apply on the tasks."""
        self.basic_commands_object.display_commands()
        print('mn - modify name | md - modify date')
        print('-'*self.width)


class TasksUIOptionalCommands(TasksUIBasicCommands):
    """For LSP."""
    
    def __init__(self):
        super().__init__()

    def display_optional_task_commands(self):
        """Gives a list of optional commands to apply on the tasks."""
        
        print('-'*self.width)
        print('X - delete every task | U - delete one task')
        print('-'*self.width)