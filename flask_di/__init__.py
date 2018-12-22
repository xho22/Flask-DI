from typing import Type, List, Callable, Dict, Any
from functools import wraps
from flask import Flask, _app_ctx_stack


class DependencyUnresolvableException(Exception):
    pass


class WrongProviderObjectException(Exception):
    pass


class Provider:
    _provides = None
    _instance = None

    def provide(self):
        raise NotImplementedError()

    def get_provided_object_name(self) -> str:
        return self.__class__.__name__.replace("Provider", "") if self._provides is None else self._provides


class Resolver:
    @staticmethod
    def get_function_dependencies(func: Callable) -> Dict:
        dependencies = {}
        for name, class_type in func.__annotations__.items():
            if name == 'return':
                continue
            dependencies[name] = class_type.__name__

        return dependencies


class ServiceLocator:
    def __init__(self):
        self.provider = {}

    def register_provider(self, provider: Type[Provider]) -> None:
        init_flag = True
        for p_name, p_instance in self.provider.items():
            if type(p_instance) == provider:
                init_flag = False
                break
        if init_flag:
            provider_instance = provider()
            self.provider[provider_instance.get_provided_object_name()] = provider_instance

    def resolve(self, dependency) -> Any:
        dep = self.provider.get(dependency)  # type: Provider
        if not dep:
            raise DependencyUnresolvableException("{} could not be resolved.".format(dependency))

        return dep.provide()


class DI:
    def __init__(self, app: Flask = None, provider: List[Type[Provider]] = None):
        self._app = app
        self._provider = provider
        if app is not None:
            self.init_app(app, provider)

    def init_app(self, app: Flask, provider: List[Type[Provider]]):
        self._app = app
        self._provider = provider
        self._app.before_request(self._attach_to_request)

    def _attach_to_request(self):
        if self._provider is not None:
            for p in self._provider:
                if not issubclass(p, Provider):
                    raise WrongProviderObjectException("Provider need to subclass the Provider class.")
                self.get_service_locator().register_provider(p)

    # hold singleton ServiceLocator
    __current_service_locator = None

    @staticmethod
    def get_service_locator() -> ServiceLocator:
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'flask_di'):
                if DI.__current_service_locator is None:
                    DI.__current_service_locator = ServiceLocator()
                ctx.flask_di = DI.__current_service_locator
            return ctx.flask_di


def inject(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        di = DI.get_service_locator()
        for param, obj in Resolver().get_function_dependencies(func).items():
            resolved = di.resolve(obj)
            if resolved not in args:
                kwargs[param] = resolved
        return func(*args, **kwargs)

    return func_wrapper


def singleton(func):
    @wraps(func)
    def func_wrapper(self, *args, **kwargs):
        if self._instance is None:
            self._instance = func(self, *args, **kwargs)
        return self._instance
    return func_wrapper
