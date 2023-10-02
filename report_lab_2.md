# Laboratory work #2: Task Management System Using Creational Design Patterns

## Author: Frunze Vladislav
## Group: FAF-212

## Objectives:

* Study and understand the Creational Design Patterns. 
* Choose a domain, define its main classes/models/entities and choose the appropriate instantiation mechanisms. 
* Use some creational design patterns for object instantiation in a sample project.

## Used Design Patterns:
* Factory Method
* Prototype
* Singleton
* Builder

## Implementation
In this laboratory work, I continue to develope the terminal-based Task Management System (TMS) from the previous laboratory.

### Factory Method
I have implemented the Factory design pattern in two ways. First, I have created two types of users, protected (with password) and simple (without password). The protected user has its data encrypted by the "PasswordManger" using Ceasar's cipher with permutation using the 93 common characters. Thus, if you want to use the TMS you can write the login and if you want your data to be protected you write a password, otherwise, you can click enter and the TMS will create a simple user. In this way, the factory method chooses what type of object to create "ProtectedUser" or "SimpleUser".

Example:
```
class UserFactory:
    def create_user(self, user_name, password):
        if password:
            return ProtectedUser(user_name, password)
        else:
            return SimpleUser(user_name) 
``` 

The second way that I have implemented the Factory design pattern is by choosing which manager to create the one for tasks or the one for objectives.

Example:
```
class ManagerFactory:
    def create(self, manager, user_data):
        if manager == "objectives":
            return ObjectivesManager(user_data)
        elif manager == "tasks":
            return TasksManager(user_data)
```

### Prototype
Next, I have integrated the prototype design pattern. I applied it on the "TasksUIBasicCommands", as this specific class may be needed to be cloned in the case that I will implement the subtasks for each task, which will require the same options. So, in order to not create the object again I could just clone it. This is done by the "clone" function below.

Example:
```
class TasksUIBasicCommands(Commands):
        def __init__(self):
            self.width = 49

        def display_commands(self):
            print('-'*self.width)
            print('< back | + add | - delete | m - modify')
            print('-'*self.width)
        
        def clone(self):
            obj = TasksUIBasicCommands()
            obj.width = self.width
            return obj
```

### Singleton
Further, I have used the singleton design pattern, which assures that you will have only an instance of a class, and it will be global. I integrated it by creating a "metaclass" which will be called each time a class related to it is instantiated. The metaclass then checks if the class has been already instantiated, if it has it will return the same instance, otherwise, it will create an instance and add it to a dictionary to keep track of it. In my case, the metaclass is used by the password manager, databases manager, and other classes.


Example:
```
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class PasswordManager(metaclass=SingletonMeta):
...
```


### Builder
The builder design pattern I applied on layers of the application, that is, the objectives and tasks pages. First, I defined the product I want to obtain which is a page with header, body, and footer. Next, I defined the abstract class of the builder, which will have the "create_header", "create_body", and "create_footer" methods. Then, I wrote two builders for the objectives page, and the tasks page.

Example:
```
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
    def __init__(self, user_data):
        self.product = Page()
        self.user_data = user_data

    def create_header(self):
        self.product.header = Header(self.user_data)

    def create_body(self):
        self.product.body = ObjectivesUIList(self.user_data)

    def create_footer(self):
        self.product.footer = ObjectivesUIBasicCommands()

    def get_page(self):
        return self.product


class TasksPageBuilder(PageBuilder):
    def __init__(self, user_data):
        self.product = Page()
        self.user_data = user_data

    def create_header(self):
        self.product.header = Header(self.user_data)

    def create_body(self):
        self.product.body = TasksUIList(self.user_data)

    def create_footer(self):
        self.product.footer = TasksUIBasicCommands()

    def get_page(self):
        return self.product
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
1 - Present TMPS lab 2 - Today
2 - Present CS lab 2 - Today
-------------------------------------------------
< back | + add | - delete | m - modify
-------------------------------------------------
Command: 
```

### Conclusions:
Creational design patterns are great for organizing your code, especially when it comes to instantiation. They help you bring more flexibility to your app, and push you to maintain the SOLID principles.