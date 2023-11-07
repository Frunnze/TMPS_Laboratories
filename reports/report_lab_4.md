# Laboratory work #4: Task Management System Using Behavioural Design Patterns

## Author: Frunze Vladislav
## Group: FAF-212

## Objectives:
* Study and understand the Behavioral Design Patterns. 
* As a continuation of the previous laboratory work, think about what communication between software entities might be involed in your system. 
* Create a new Project or add some additional functionalities using behavioral design patterns.

## Used Design Patterns:
* Command
* Strategy
* Memento

## Implementation
In this laboratory work, I continue to develope the terminal-based Task Management System (TMS) from the previous laboratories.

### Command

Command is a behavioral design pattern that turns a request into a stand-alone object that contains all information about the request. This transformation lets you pass requests as a method arguments, delay or queue a request’s execution, and support undoable operations.

To implement it, we have to define an interface with the "execute" method, an "Invoker" class that will trigger the command, and concrete commands classes that have as a reference a class that implements the command itself.
Example:
```
class Command(ABC):
    """Interface"""
    @abstractmethod
    def execute(self):
        pass


class Invoker:
    def __init__(self, command):
        self._command = command

    def execute_command(self):
        self._command.execute()


class AddObjective(Command):
    """Concrete command"""
    def __init__(self, receiver, objective_name):
        self.receiver = receiver
        self.objective_name = objective_name

    def execute(self):
        self.receiver.add(self.objective_name)


class DeleteObjective(Command):
    """Concrete command"""
    def __init__(self, receiver, objective_number):
        self.receiver = receiver
        self.objective_number = objective_number

    def execute(self):
        self.receiver.delete(self.objective_number)
``` 

### Strategy

Strategy is a behavioral design pattern that lets you define a family of algorithms, put each of them into a separate class, and make their objects interchangeable.

To implement it in my project, I defined the strategy interface, the context class, which as a reference will have one of the chosen strategies, and the strategies themselves, which in my case are ciphers.
Example:
```
# Strategy design pattern
class SecurityContext:
    """Context"""

    def __init__(self, strategy):
        self.strategy = strategy

    def encrypt(self, message, key1, key2):
        return self.strategy.encrypt(message, key1, key2)

    def decrypt(self, encrypted_message, key1, key2):
        return self.strategy.decrypt(encrypted_message, key1, key2)
    

class SecurityStrategy(ABC):
    """Strategy interface."""

    @abstractmethod
    def encrypt():
        pass

    @abstractmethod
    def decrypt():
        pass


class VigenereCipherAdapter(SecurityStrategy):
    """Strategy 1"""

    def __init__(self, vigenere_object):
        self.vigenere = vigenere_object

    def encrypt(self, message, key1, key2):
        self.vigenere.key = key2
        return self.vigenere.get_ciphertext(message)
    
    def decrypt(self, encrypted_message, key1, key2):
        self.vigenere.key = key2
        return self.vigenere.get_message(encrypted_message)


class CaesarCipher(SecurityStrategy):
    """Strategy 2: Encrypts and decrypts the data."""
    ...
``` 

### Memento

Memento is a behavioral design pattern that lets you save and restore the previous state of an object without revealing the details of its implementation.

To implement it, I have created a class "Memento", which holds the state of an object, then I created the class "Caretaker", which will be something similar to a list of mementos. And finally, the originators that I chose were the "ObjectsManager" and "TasksManager".
Example:
```
class Memento:
    """Represents the state of the originator"""

    def __init__(self, originator, user_data, db, user):
        self.originator = originator
        self.user_data = user_data
        self.db = db
        self.user = user

    def restore(self):
        self.originator.user_data = self.user_data
        self.originator.db = self.db
        self.originator.user = self.user
        self.db.save_user_data(self.user, self.user_data)


class Caretaker:
    def __init__(self):
        self.mementos = []

    def add_memento(self, memento):
        self.mementos.append(memento)

    def get_memento(self):
        if self.mementos:
            return self.mementos.pop()
        else:
            return None


class ObjectivesManager(Manager):
    """Manages the objectives."""

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
1 - obj 1
2 - obj 2
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
-------------------------------------------------
< back | + add | - delete | m - modify
-------------------------------------------------
mn - modify name | md - modify date | u - undo
-------------------------------------------------
Command: 
```

### Conclusions:
The Behavioural Design Patterns are helpful in creating scalable and flexible systems in which the objects can communicate between themselves efficiently. In my project, they helped in improving the functionality and the security.