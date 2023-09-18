# Laboratory work #1: Task Management System Using SOLID Principles

## Author: Frunze Vladislav
## Group: FAF-212

## Objectives:

* Study and understand the SOLID Principles.
* Choose a domain, define its main classes/models/entities and choose the appropriate instantiation mechanisms.
* Create a sample project that respects SOLID Principles.


## Implementation
In this laboratory work, I have implemented a terminal-based Task Management System (TMS). As it became, a relatively large project, I will list the SOLID principles, give an example, and explain how it works in the TMS.

### Single-Responsibility Principle (SRP)
The below example represents the databases class, which has only one responsibility to handle (retrieve and store) the user data. The user data is just a nested dictionary with user data such as user name, objectives, and tasks. It stores and retrieves this data to and from a .txt file in the "DB" directory.

Example:
```
class DB(DataSource):
    def get_user_data(self, user):  
        try:
            with open(f'Lab1/DB/{user.name}.txt', 'r') as file:
                file_data = file.read()
                return eval(file_data)
        except FileNotFoundError:
            return {'user_name': user.name, 'objectives': []}

    def save_user_data(self, user_data):
        with open(f'Lab1/DB/{user_data["user_name"]}.txt', 'w') as file:
            file.write(str(user_data))
```

### Open-Closed Principle (OCP)
The project contains several examples where this principle is used, however, I think the most necessary is the below one. As I said, the TMS is terminal-based. It has 3 main "UIs". The login UI, Objectives UI, and Tasks UI. The last two have several commands that the user could apply to the objectives or tasks, like add, delete, modify, etc. Thus, as the project is developed there may appear the need for other commands. To accomplish it and satisfy the OCP principle we cannot modify the classes below. What we can do, Is to create an abstract class that will ensure that the "display_commands" method will be implemented, and just create another class with more commands for each UI.

Example:
```
class Commands(ABC):
    @abstractmethod
    def display_commands(self):
        pass

class ObjectivesUIBasicCommands(Commands):
        def __init__(self):
            self.width = 49

        def display_commands(self):            
            print('-'*self.width)
            print('< back | + add | - delete | o - open | m - modify')
            print('-'*self.width)

class TasksUIBasicCommands(Commands):
        def __init__(self):
            self.width = 49

        def display_commands(self):            
            print('-'*self.width)
            print('< back | + add | - delete | m - modify')
            print('-'*self.width)
```

### Liskov Substitution Principle (LSP)
LSP is simple. It says that if you take an object of a child class and replace it with an object of the parent class the program should run correctly. In the below example, we have two classes "TasksUIBasicCommands" and "TasksUIOptionalCommands". The second one inherits from the first one. This means that if we use an object of the second class instead of an object of the first one, with the "display_commands" method, the program will just run the method from the first class, even though it is placed in the first class. Thus, the program will run correctly without unexpected behaviors.

Example:
```
class TasksUIBasicCommands:
        def __init__(self):
            self.width = 49

        def display_commands(self):            
            print('-'*self.width)
            print('< back | + add | - delete | m - modify')
            print('-'*self.width)


class TasksUIOptionalCommands(TasksUIBasicCommands):
        def __init__(self):
            super().__init__()

        def display_optional_task_commands(self):            
            print('-'*self.width)
            print('X - delete every task')
            print('-'*self.width)
```


### Interface Segregation Principle (ISP)
One simple example of how the ISP was used in this project is the below one. It represents two abstract classes. First ensures that the lists (objectives in the second UI, and tasks in the third UI) will be listed correctly. The second class ensures that the commands for each mentioned UI will be displayed correctly. Now, I could have written only one abstract class that ensured everything mentioned, however, in this case, a class that depends on it has to implement other unnecessary methods. Thus, the ISP and SRP would be broken.

Example:
```
class Lists(ABC):
    def __init__(self, user_data):
        self.user_data = user_data

    @abstractmethod
    def display_list(self):
        pass

class Commands(ABC):
    @abstractmethod
    def display_commands(self):
        pass
```

### Dependency Inversion Principle (DIP)
As we know, DIP suggests that high-level modules should not depend on low-level modules but on abstractions. This is a great idea if you want to create a scalable system. In this project, I used this principle in the following way, represented in the example. In this case, our "high-level module" consists of several classes (only one mentioned in the example): ObjectivesUIList, TasksUIList, TasksManager, and ObjectivesManager. All these classes receive the data from the database object. Thus, they depend on the DB class directly, which they should not because we could scale the system to use APIs to get the data, and in this way, we won't be able to. Therefore, we create an abstract class, which has a mandatory method called "get_user_data". We make our DB class inherit from it, and in the future the API class as well. Now, our high-level modules can receive data from several data sources, without worrying that it might not be received.

Example:
```
class ObjectivesUIList(Lists):
    def __init__(self, user_data):
        self.user_data = user_data
        self.width = 49


    def display_list(self):
        ...

class DataSource(ABC):
    @abstractmethod
    def get_user_data(self):
        pass

class DB(DataSource):
    def get_user_data(self, user):  
        ...
        
    def save_user_data(self, user_data):
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
User: Vlad
-------------------------------------------------
Objectives: 
-------------------------------------------------
1 - Finish university
2 - Develop my programming skills
3 - Read more
-------------------------------------------------
< back | + add | - delete | o - open | m - modify
-------------------------------------------------
Command: 
```


### Result 3: Tasks UI

```
User: Vlad
-------------------------------------------------
Objective: Finish university
Tasks: 
-------------------------------------------------
1 - Present TMPS lab 1 - Today
2 - Present CS lab 1 - Today
-------------------------------------------------
< back | + add | - delete | m - modify
-------------------------------------------------
Command: 
```

### Conclusions:
SOLID principles are a necessary tool in developing software. It makes the code more readable, testable and organized. Large software without these principles would be almost impossible to change, scale, and understand.