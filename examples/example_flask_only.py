from flask import Flask
from flask_di import DI, inject, Provider


class UserRepository:
    def get_all(self):
        return [
            {"first_name": "Bob", "last_name": "Smith"},
            {"first_name": "Mary", "last_name": "Lou"}
        ]


class UserRepositoryProvider(Provider):
    def provide(self):
        return UserRepository()


app = Flask(__name__)
di = DI(app, [
    UserRepositoryProvider
])


@app.route("/")
@inject
def example_1(user_repository: UserRepository):
    output = ""
    for user in user_repository.get_all():
        output = output + "{} {}<br>".format(user["first_name"], user["last_name"])
    return output


@app.route("/user/<first_name>")
@inject
def example_2(first_name, user_repository: UserRepository):
    first_names = [u["first_name"] for u in user_repository.get_all()]
    if first_name in first_names:
        return "{} was found in user list".format(first_name)
    else:
        return "{} is unknown".format(first_name)
