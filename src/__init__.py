from flask import Flask, render_template

from data.database.database import mongo, mysql


def create_app():
    my_app = Flask(__name__)
    my_app.config.from_pyfile('config.py')
    my_app.config['MONGODB_SETTINGS'] = {
        'db': 'xupei',
        'host': '222.186.10.246',
        'port': 27017,
        'username': 'xupei',
        'password': 'mongo'
    }
    mongo.init_app(my_app)
    mysql.init_app(my_app)

    return my_app


app = create_app()

from . import controller_v1, controller_v2


@app.route('/api')
def send_api_html():
    return render_template('api.html')
