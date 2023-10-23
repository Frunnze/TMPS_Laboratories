# Laboratory work #3: Task Management System Using Structural Design Patterns

## Author: Frunze Vladislav
## Group: FAF-212

## Objectives:
* Study and understand the Structural Design Patterns.
* As a continuation of the previous laboratory work, think about the functionalities that your system will need to provide to the user.
* Implement some additional functionalities using structural design patterns.

## Used Design Patterns:
* Adapter
* Proxy
* Decorator
* Bridge

## Implementation
In this laboratory work, I continue to develope the terminal-based Task Management System (TMS) from the previous laboratories.

### Adapter

Adapter design pattern helps you use classes with the same objective but which are not compatible with the interface that you have. Thus, to solve this, we create another class that "adapts" the foreign class for your interface. Below is an example of how I used a foreign class of an encryption method, and adapted it to the security interface that I had.
Example:
```
class Security(ABC):
    @abstractmethod
    def encrypt():
        pass

    @abstractmethod
    def decrypt():
        pass

class VigenereCipherAdapter(Security):
    def __init__(self, vigenere_object):
        self.vigenere = vigenere_object

    def encrypt(self, message, key1, key2):
        self.vigenere.key = key2
        return self.vigenere.get_ciphertext(message)
    
    def decrypt(self, encrypted_message, key1, key2):
        self.vigenere.key = key2
        return self.vigenere.get_message(encrypted_message)


class VigenereCipher:
    def __init__(self, key):
        self.key = key
    
    ...
``` 

### Proxy

Proxy design pattern is a great way to control access to an object. Generally, this object needs privacy or uses lots of resources, thus needs to have access control to it. Below I used this design pattern in order to secure my whole application with a general password.
Example:
```
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
``` 

### Decorator

Decorator suggests adding new functionality to an already created object dynamically. So, we basically wrap the object into another object which adds these functionalities to it. Below, I used a decorator to identify whether the user is protected or not by adding to the header object a new line that shows the corresponding information. Also, I added a decorator in order to add 2 new commands for the tasks page: modify name, and modify date. 
Example:
```
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


class TasksUICommandsDecorator:
    def __init__(self, basic_commands_object):
        self.width = 49
        self.basic_commands_object = basic_commands_object

    def display_commands(self):
        """Gives a list of commands to apply on the tasks."""
        self.basic_commands_object.display_commands()
        print('mn - modify name | md - modify date')
        print('-'*self.width)
``` 

### Bridge

Bridge design pattern tries to distinguish the abstraction (control layer) from the implementation. It does this by creating a class for abstraction, which takes as an attribute one of the implementations (classes that do something). Also, we have an interface that tells each implementation class what methods are mandatory. In this way, we can extend the abstraction class and implementation classes independently. Below, I used this design pattern for the security.
Example:
```
class SecurityAbstraction:
    """The abstraction"""

    def __init__(self, security_impl):
        self.security_impl = security_impl

    def encrypt(self, message, key1, key2):
        return self.security_impl.encrypt(message, key1, key2)

    def decrypt(self, encrypted_message, key1, key2):
        return self.security_impl.decrypt(encrypted_message, key1, key2)


class Security(ABC):
    """Implementation interface."""

    @abstractmethod
    def encrypt():
        pass

    @abstractmethod
    def decrypt():
        pass


class VigenereCipherAdapter(Security):
    """Implementation 1"""

    def __init__(self, vigenere_object):
        self.vigenere = vigenere_object

    def encrypt(self, message, key1, key2):
        self.vigenere.key = key2
        return self.vigenere.get_ciphertext(message)
    
    def decrypt(self, encrypted_message, key1, key2):
        self.vigenere.key = key2
        return self.vigenere.get_message(encrypted_message)


class CaesarCipher(Security):
    """Implimentation 2"""
    ...
``` 

## Conclusions / Screenshots / Results
### Result 1: Login UI

```
Welcome to the Task Management System!
Login: 
```

### Result 2: Objectives UI

```
Protected
-------------------------------------------------
User: user
-------------------------------------------------
Objectives: 
-------------------------------------------------
1 - Finish university
2 - Travel
-------------------------------------------------
< back | + add | - delete | o - open | m - modify
-------------------------------------------------
Command: 
```


### Result 3: Tasks UI

```
Protected
-------------------------------------------------
User: user
-------------------------------------------------
Objective: Finish university
Tasks: 
-------------------------------------------------
1 - task1 - tomorrow
2 - task3 - today
3 - Present TMPS lab 3 - today
-------------------------------------------------
< back | + add | - delete | m - modify
-------------------------------------------------
mn - modify name | md - modify date
-------------------------------------------------
Command: 
```

### Conclusions:
The structural design patterns are helpful in creating scalable and flexible systems. They help with compatibility between old and new systems. In my project, they helped in improving the functionality and the security.