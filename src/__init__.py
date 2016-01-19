
from flask import Flask

from data.database.database import mongo, mysql


def create_app():
    my_app = Flask(__name__)
    my_app.config.from_pyfile('config.py')

    mongo.init_app(my_app)
    mysql.init_app(my_app)

    return my_app


app = create_app()

from . import controller
