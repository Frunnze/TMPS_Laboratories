"""Code for user interaction."""

from abc import ABC, abstractmethod

from domain.models.UI import *
from domain.factory import UserFactory, ManagerFactory
from domain.models.logic import *


class AppProxy:
    def __init__(self, app) -> None:
        self.app = app

    def run(self):
        print('\n'*50)
        entered = input("App password: ")
        password = 'app123'
        while entered != password:
            print('\n'*50)
            entered = input("App password: ")
        else:
            self.app.run()


class App:
    """The class of the application."""

    def __init__(self):
        self.login_ui  = LoginUI()
        self.user_factory = UserFactory()
        self.manager_factory = ManagerFactory()


    def run(self):
        """Runs the application, and interacts with the user."""

        self.user_data = None
        while not self.user_data:
            user_name, password = self.login_ui.login()
            user = self.user_factory.create_user(user_name, password)

            # Choose the security strategy
            if len(password) < 5:
                strategy = VigenereCipherAdapter(VigenereCipher(None))
            else:
                strategy = CaesarCipher()
            self.db = DB(SecurityContext(strategy))

            self.user_data = self.db.get_user_data(user)
       
        header_object = HeaderDecorator(Header(self.user_data), password)
        objectives_page_builder = ObjectivesPageBuilder(
            header=header_object, 
            objectives=ObjectivesUIList(self.user_data),
            commands=ObjectivesUIBasicCommands())
        objectives_page_builder.create_header()
        objectives_page_builder.create_body()
        objectives_page_builder.create_footer()
        self.objectives_page = objectives_page_builder.get_page()

        tasks_page_builder = TasksPageBuilder(
            header=header_object,
            tasks=TasksUIList(self.user_data),
            commands=TasksUICommandsDecorator(TasksUIBasicCommands()))
        tasks_page_builder.create_header()
        tasks_page_builder.create_body()
        tasks_page_builder.create_footer()
        self.tasks_page = tasks_page_builder.get_page()


        self.tasks_manager = self.manager_factory.create("tasks", self.db, user)
        self.objectives_manager = self.manager_factory.create("objectives", self.db, user)
        
        self.objectives_page.display_page(self.user_data)

        tasks_caretaker = Caretaker()
        objectives_caretaker = Caretaker()

        opened_tasks_ui = False
        while True:
            command = input('Command: ')
            if not opened_tasks_ui:
                if command == '<':
                    self.user_data = None
                    while not self.user_data:
                        user_name, password = self.login_ui.login()
                        user = self.user_factory.create_user(user_name, password)

                        # Choose the security strategy
                        if len(password) < 5:
                            strategy = VigenereCipherAdapter(VigenereCipher(None))
                        else:
                            strategy = CaesarCipher()
                        self.db.password_manager = SecurityContext(strategy)

                        self.user_data = self.db.get_user_data(user)

                    tasks_caretaker = Caretaker()
                    objectives_caretaker = Caretaker()

                    self.objectives_manager.user, self.tasks_manager.user = user, user
                    self.objectives_manager.db, self.tasks_manager.db = self.db, self.db
                    self.objectives_page.header.password = password
                    self.objectives_page.display_page(self.user_data)
                elif command == '+':
                    memento = self.objectives_manager.save()
                    objectives_caretaker.add_memento(memento)

                    objective_name = input(' '*3 + 'Objective name: ')

                    request = AddObjective(
                        receiver=self.objectives_manager, 
                        objective_name=objective_name
                    )
                    Invoker(request).execute_command()

                    self.user_data = self.db.get_user_data(user)
                    self.objectives_page.display_page(self.user_data)
                elif command == '-':
                    memento = self.objectives_manager.save()
                    objectives_caretaker.add_memento(memento)

                    objective_number = input(' '*3 + 'Objective number: ')

                    request = DeleteObjective(
                        receiver=self.objectives_manager, 
                        objective_number=objective_number
                    )
                    Invoker(request).execute_command()

                    self.user_data = self.db.get_user_data(user)
                    self.objectives_page.display_page(self.user_data)
                elif command == 'o':
                    objective_number = input(' '*3 + 'Objective number: ')
                    self.user_data = self.db.get_user_data(user)
                    self.tasks_page.body.obj_num = objective_number
                    self.tasks_page.display_page(self.user_data)
                    self.tasks_manager.user_data = self.db.get_user_data(user)
                    opened_tasks_ui = True
                    tasks_caretaker = Caretaker()
                elif command == 'm':
                    memento = self.objectives_manager.save()
                    objectives_caretaker.add_memento(memento)

                    objective_number = input(' '*3 + 'Objective number: ')
                    new_title = input(' '*3 + 'New title: ')

                    request = ModifyObjective(
                        receiver=self.objectives_manager, 
                        objective_number=objective_number,
                        objective_title=new_title
                    )
                    Invoker(request).execute_command()

                    self.user_data = self.db.get_user_data(user)
                    self.objectives_page.display_page(self.user_data)
                elif command == 'u':
                    memento = objectives_caretaker.get_memento()
                    if memento:
                        memento.restore()
                        self.objectives_page.display_page(memento.user_data)
            else:
                if command == '<':
                    self.user_data = self.db.get_user_data(user)
                    self.objectives_manager.user_data = self.user_data
                    self.objectives_page.display_page(self.user_data)
                    opened_tasks_ui = False
                elif command == '+':
                    memento = self.tasks_manager.save()
                    tasks_caretaker.add_memento(memento)

                    task_title = input(' '*3 + 'Task name: ')
                    due_date = input(' '*3 + 'Due date: ')

                    request = AddTask(
                        receiver=self.tasks_manager, 
                        task_title=task_title,
                        due_date=due_date, 
                        objective_number=objective_number
                    )
                    Invoker(request).execute_command()

                    self.user_data = self.db.get_user_data(user)
                    self.tasks_page.body.obj_num = objective_number
                    self.tasks_page.display_page(self.user_data)
                elif command == '-':
                    memento = self.tasks_manager.save()
                    tasks_caretaker.add_memento(memento)

                    task_number = input(' '*3 + 'Task number: ')

                    request = DeleteTask(
                        receiver=self.tasks_manager, 
                        task_number=task_number,
                        objective_number=objective_number
                    )
                    Invoker(request).execute_command()

                    self.user_data = self.db.get_user_data(user)
                    self.tasks_page.body.obj_num = objective_number
                    self.tasks_page.display_page(self.user_data)
                elif command == 'm':
                    memento = self.tasks_manager.save()
                    tasks_caretaker.add_memento(memento)

                    task_number = input(' '*3 + 'Task number: ')
                    new_title = input(' '*3 + 'New title: ')
                    new_dd = input(' '*3 + 'New due date: ')

                    request = ModifyTask(
                        receiver=self.tasks_manager, 
                        new_title=new_title,
                        new_dd=new_dd,
                        task_number=task_number, 
                        objective_number=objective_number
                    )
                    Invoker(request).execute_command()

                    self.user_data = self.db.get_user_data(user)
                    self.tasks_page.body.obj_num = objective_number
                    self.tasks_page.display_page(self.user_data)
                elif command == 'mn':
                    memento = self.tasks_manager.save()
                    tasks_caretaker.add_memento(memento)

                    task_number = input(' '*3 + 'Task number: ')
                    new_title = input(' '*3 + 'New title: ')

                    request = ModifyTaskName(
                        receiver=self.tasks_manager, 
                        new_title=new_title,
                        task_number=task_number, 
                        objective_number=objective_number
                    )
                    Invoker(request).execute_command()

                    self.user_data = self.db.get_user_data(user)
                    self.tasks_page.body.obj_num = objective_number
                    self.tasks_page.display_page(self.user_data)
                elif command == 'md':
                    memento = self.tasks_manager.save()
                    tasks_caretaker.add_memento(memento)

                    task_number = input(' '*3 + 'Task number: ')
                    new_dd = input(' '*3 + 'New due date: ')

                    request = ModifyTaskDate(
                        receiver=self.tasks_manager, 
                        new_dd=new_dd,
                        task_number=task_number, 
                        objective_number=objective_number
                    )
                    Invoker(request).execute_command()

                    self.user_data = self.db.get_user_data(user)
                    self.tasks_page.body.obj_num = objective_number
                    self.tasks_page.display_page(self.user_data)
                elif command == 'u':
                    memento = tasks_caretaker.get_memento()
                    if memento:
                        memento.restore()
                        self.tasks_page.display_page(memento.user_data)


my_app = AppProxy(App())
my_app.run()