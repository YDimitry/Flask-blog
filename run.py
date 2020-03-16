#
# https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-one

import os

from app import create_app

config_name = os.getenv('FLASK_ENV')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()

