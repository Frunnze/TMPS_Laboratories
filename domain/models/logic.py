"""
Containts the classes that represent the core concepts of the
task management system.
"""

from abc import ABC, ABCMeta, abstractmethod


class SingletonMeta(type):
    """
    Singleton metaclass, which assures that an object is not going
    to be repeated in the program.
    """

    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    

class CustomMeta(SingletonMeta, ABCMeta): pass
class DataSource(metaclass=CustomMeta):
    """Ensures that the objects will receive the data."""
    @abstractmethod
    def get_user_data(self):
        pass


class DB(DataSource):
    """Deals with the user data."""
    
    def __init__(self):
        self.password_manager = PasswordManager()


    def get_user_data(self, user):  
        """Extract the user data from the .txt file as a dictionary."""  
        try:
            with open(f'DB/{user.name}.txt', 'r') as file:
                file_data = file.read()
                if user.password is None:
                    if user.name in file_data:
                        try:
                            return eval(file_data)
                        except Exception:
                            return None
                    else:
                        return None
                else:
                    file_data = self.password_manager.decrypt(
                        file_data, len(user.password), user.password)
                    print(file_data)
                    if user.name in file_data:
                        try:
                            return eval(file_data)
                        except Exception:
                            return None
                    else:
                        return None
        except FileNotFoundError:
            return {'user_name': user.name, 'objectives': []}
        

    def save_user_data(self, user, user_data):
        """Save the user data in the .txt file."""

        with open(f'DB/{user_data["user_name"]}.txt', 'w') as file:
            if user.password:
                encrypted_user_data = self.password_manager.encrypt(
                    str(user_data), len(user.password), 
                    user.password)
                file.write(encrypted_user_data)
            else:
                file.write(str(user_data))
    

class PasswordManager(metaclass=SingletonMeta):
    """Encrypts and decrypts the data."""

    def __init__(self):
        self.alphabet = """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}|;:'\",.<>?/\\ """


    def encrypt(self, message, key1, key2=''):
        """Encrypts the given message with Caesar's cipher using the given keys."""

        # Makes a new alphabet order, if we have key2.
        if key2:
            new_alphabet = ''.join(dict.fromkeys(key2 + self.alphabet))

        # Associates letters to the indices of letters used to encrypt the message.
        map = {letter: (index + key1) % 93 for index, letter in enumerate(new_alphabet)}

        # Encrypts the message.
        encrypted_message = ''
        for letter in message:
            encrypted_message += new_alphabet[map[letter]]

        return encrypted_message


    def decrypt(self, encrypted_message, key1, key2=''):
        """Decrypts the given encrypted message."""

        # Makes a new alphabet order, if we have key2.
        if key2:
            new_alphabet = ''.join(dict.fromkeys(key2 + self.alphabet))

        # Associates letters to the indices of letters used to decrypt the message.
        map = {letter: (index - key1) % 93 for index, letter in enumerate(new_alphabet)}

        # Decrypts the message.
        decrypted_message = ''
        for letter in encrypted_message:
            decrypted_message += new_alphabet[map[letter]]

        return decrypted_message


class User(ABC):

    @abstractmethod
    def change_name(self):
        pass

class SimpleUser(User):
    """Defines the properties of the user."""

    def __init__(self, name):
        self.name = name
        self.password = None

    def change_name(self, new_name, user_data):
        """Change the name of the user."""
        
        user_data['user_name'] = new_name
        
        return user_data


class ProtectedUser(User):
    """Defines the properties of the user."""

    def __init__(self, name, password):
        self.name = name
        self.password = password
    
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
        return self.user_data


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

        return self.user_data