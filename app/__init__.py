from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template


from config import app_config

db = SQLAlchemy()


def create_app(conf_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[conf_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    @app.route('/')
    def hello_world():
        conf_var = app.config
        return render_template('index.html',conf=conf_var)



    return app
