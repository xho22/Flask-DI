Flask-DI - type hinting based dependency injection for Flask and Python >=3.5
==================================================================

Introduction
------------
Dependency injection is a technique that seems rather unpopular in Python, probably
because Python offers some other ways to deal with the related problems. I still
consider traditional dependency injection good software craftsmanship and was
looking for a quick and simple way to inject dependencies into my Flask applications using Pythons
newest type hinting features.

```python
pip install Flask-DI
```


Getting started
---------------
To use Flask-DI, you only need to follow these simple steps:
- Define a `Provider` class for the dependency that you want to inject. For this example, lets assume that we put
the logic for saying "Hello World" into a separate Service class:
```python
from flask_di import Provider

class HelloWorldService:
    def say_hello(self):
        return "Hello World!"
        
class HelloWorldServiceProvider(Provider):
    def provide(self):
        return HelloWorldService()
```
By default, Flask-DI expects the Provider class to be named like the dependency it is supposed to provide, plus the
`Provider` postfix. If you had a class named `UserRepository`, the expected Provider class name 
would be `UserRepositoryProvider`. If you want to choose a different class name, just use the `_provides` class
variable:

```python
from flask_di import Provider

class TotallyRandomClassName(Provider):
    _provides = "HelloWorldService"
    
    def provide(self):
        return HelloWorldService()
```

If you don't want to create a new instance of `HelloWorldService` every time, you can use the `@singleton` decorator
on `provide()`:

```python
from flask_di import Provider, singleton

class TotallyRandomClassName(Provider):
    _provides = "HelloWorldService"
    
    @singleton
    def provide(self):
        return HelloWorldService()
```

- Initialize the Flask-DI extension and register all your `Provider` classes:
```python
from flask import Flask
from flask_di import DI

app = Flask(__name__)
di = DI(app, [HelloWorldServiceProvider])
```

- Use type hinting and the `@inject` decorator to inject your dependencies into your functions:

```python
@app.route('/')
@inject
def hello_world(hello_world: HelloWorldService):
    return hello_world.say_hello()
```


Examples?
---------
Please refer to the `examples` package for full examples on how to use Flask-DI within a Flask or a Flask-RESTPlus
application.