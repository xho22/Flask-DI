from flask_di import *
from flask import Flask, _app_ctx_stack
import pytest


class FakeService:
    def do_stuff(self):
        pass


class FakeServiceProvider(Provider):
    def provide(self):
        return FakeService()


class SingletonFakeServiceProvider(Provider):
    _provides = "FakeService"

    @singleton
    def provide(self):
        return FakeService()


class TestProvider:
    def test_get_own_name_returns_default_name(self):
        provider = FakeServiceProvider()

        assert provider.get_provided_object_name() == "FakeService"

    def test_get_own_name_returns_customized_name_when_set(self):
        class AnotherFakeProvider(Provider):
            _provides = "Foo"

        assert AnotherFakeProvider().get_provided_object_name() == "Foo"


class TestResolver:
    def test_get_function_dependencies(self):
        class FakeTypeA:
            pass

        def fake_function(param1: FakeTypeA) -> None:
            pass

        resolver = Resolver()
        result = resolver.get_function_dependencies(fake_function)

        assert "return" not in result
        assert "param1" in result
        assert result["param1"] == "FakeTypeA"


class TestInjector:
    def test_injector_initializes_provider_with_empty_dict(self):
        assert not ServiceLocator().provider

    def test_register_provider(self):
        injector = ServiceLocator()
        injector.register_provider(FakeServiceProvider)

        assert "FakeService" in injector.provider
        assert isinstance(injector.provider["FakeService"], FakeServiceProvider)

    def test_resolve_throws_exception_for_unknown_dependency(self):
        injector = ServiceLocator()

        with pytest.raises(DependencyUnresolvableException):
            injector.resolve("TotallyUnknownDependency")

    def test_resolve_returns_object_for_known_dependency(self):
        injector = ServiceLocator()
        injector.register_provider(FakeServiceProvider)

        result = injector.resolve("FakeService")

        assert isinstance(result, FakeService)


class TestDI:
    def test_throws_exception_when_provider_does_not_subclass_service_provider(self):
        class SomeType:
            pass

        app = Flask(__name__)
        # noinspection PyTypeChecker
        DI(app, [SomeType])

        with app.test_request_context("/"):
            with pytest.raises(WrongProviderObjectException):
                app.preprocess_request()

    def test_before_request_handler_is_attached(self):
        app = Flask(__name__)
        di = DI(app, [FakeServiceProvider])

        with app.test_request_context("/"):
            app.preprocess_request()

            assert FakeServiceProvider in di._provider
            assert "FakeService" in di.get_service_locator().provider
            assert _app_ctx_stack.top.flask_di is di.get_service_locator()


class TestInject:
    @inject
    def method_with_injection(self, service: FakeService):
        return service

    def test_inject(self):
        app = Flask(__name__)
        di = DI(app, [FakeServiceProvider])

        with app.test_request_context("/"):
            app.preprocess_request()

            result = self.method_with_injection()

            assert isinstance(result, FakeService)


class TestSingleton:
    @inject
    def method_with_injection(self, service: FakeService):
        return service

    def test_decorator_should_return_same_instance_on_every_call(self):
        app = Flask(__name__)
        di = DI(app, [SingletonFakeServiceProvider])

        with app.test_request_context("/"):
            app.preprocess_request()

            instance1 = self.method_with_injection()
            instance2 = self.method_with_injection()

            assert instance1 is instance2
