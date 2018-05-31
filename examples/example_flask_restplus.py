from flask import Flask
from flask_di import DI, inject, Provider
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api()
di = DI()


class UserRepository:
    def get_all(self):
        return [
            {"first_name": "Bob", "last_name": "Smith"},
            {"first_name": "Mary", "last_name": "Lou"}
        ]


class UserRepositoryProvider(Provider):
    def provide(self):
        return UserRepository()


class ApiProvider(Provider):
    def provide(self):
        return api


@api.route("/user")
class UserResource(Resource):
    @inject
    def __init__(self, api: Api, user_repository: UserRepository):
        super().__init__(api)
        self.user_repository = user_repository

    def get(self):
        return self.user_repository.get_all()


api.init_app(app)
di.init_app(app, [
    ApiProvider,
    UserRepositoryProvider
])
