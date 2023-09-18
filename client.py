"""Code for user interaction."""

from domain.models.logic import DB, ObjectivesManager, TasksManager
from domain.models.UI import LoginUI, ObjectivesUIList, TasksUIList, ObjectivesUIBasicCommands, TasksUIBasicCommands, TasksUIOptionalCommands
from domain.factory import UserFactory


class App:
    """The class of the application."""

    def __init__(self):
        self.lui  = LoginUI()
        self.user_name = self.lui.login()
        self.user_factory = UserFactory()
        self.user = self.user_factory.create_user(self.user_name)
        self.db = DB()
        self.user_data = self.db.get_user_data(self.user)

        self.ouil = ObjectivesUIList(self.user_data)
        self.tuil = TasksUIList(self.user_data)
        self.tm = TasksManager(self.user_data)
        self.om = ObjectivesManager(self.user_data)
        
        self.ouic = ObjectivesUIBasicCommands()
        self.tuibc = TasksUIBasicCommands()


    def run(self):
        """Runs the application, and interacts with the user."""

        self.ouil.display_list()
        self.ouic.display_commands()
        opened_tasks_ui = False
        while True:
            command = input('Command: ')
            if not opened_tasks_ui:
                if command == '<':
                    user_name = self.lui.login()
                    user = self.user_factory.create_user(user_name)
                    user_data = self.db.get_user_data(user)
                    self.ouil.user_data = user_data
                    self.ouil.display_list()
                    self.ouic.display_commands()
                    self.om.user_data = user_data
                elif command == '+':
                    objective = input(' '*3 + 'Objective name: ')
                    self.om.add(objective)
                    self.db.save_user_data(self.om.user_data)
                    self.ouil.display_list()
                    self.ouic.display_commands()
                elif command == '-':
                    objective_number = input(' '*3 + 'Objective number: ')
                    self.om.delete(objective_number)
                    self.db.save_user_data(self.om.user_data)
                    self.ouil.display_list()
                    self.ouic.display_commands()
                elif command == 'o':
                    self.tuil.user_data = self.om.user_data
                    objective_number = input(' '*3 + 'Objective number: ')
                    self.tuil.display_list(objective_number)
                    self.tuibc.display_commands()
                    opened_tasks_ui = True
                    self.tm.user_data = self.om.user_data
                elif command == 'm':
                    objective_number = input(' '*3 + 'Objective number: ')
                    new_title = input(' '*3 + 'New title: ')
                    self.om.modify(new_title, objective_number)
                    self.db.save_user_data(self.om.user_data)
                    self.ouil.display_list()
                    self.ouic.display_commands()      
            else:
                if command == '<':
                    self.ouil.display_list()
                    self.ouic.display_commands()
                    opened_tasks_ui = False
                elif command == '+':
                    task_title = input(' '*3 + 'Task name: ')
                    due_date = input(' '*3 + 'Due date: ')
                    self.tm.add(task_title, due_date, objective_number)
                    self.db.save_user_data(self.tm.user_data)
                    self.tuil.display_list(objective_number)
                    self.tuibc.display_commands()
                elif command == '-':
                    task_number = input(' '*3 + 'Task number: ')
                    self.tm.delete(task_number, objective_number)
                    self.db.save_user_data(self.tm.user_data)
                    self.tuil.display_list(objective_number)
                    self.tuibc.display_commands()
                elif command == 'm':
                    task_number = input(' '*3 + 'Task number: ')
                    new_title = input(' '*3 + 'New title: ')
                    new_dd = input(' '*3 + 'New due date: ')
                    self.tm.modify(new_title, new_dd, task_number, objective_number)
                    self.db.save_user_data(self.tm.user_data)
                    self.tuil.display_list(objective_number)
                    self.tuibc.display_commands()


my_app = App()
my_app.run()