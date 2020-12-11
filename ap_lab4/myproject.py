from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab.db'
db = SQLAlchemy(application)

#from models import User


@application.route('/')
def hello():
    return "Hello World!"


@application.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    application.run(debug=True)