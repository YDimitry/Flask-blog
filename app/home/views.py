from flask import render_template
from . import home


@home.route('/')
def homepage():
    return render_template('index.html')
