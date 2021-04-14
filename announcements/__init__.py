import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate, MigrateCommand
from flask_bcrypt import Bcrypt
from flask_cors import CORS

UPLOAD_FOLDER = './upload'
# 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

application = Flask(__name__, template_folder='../templates')

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../lab.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = 'very-secret-key'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
logging.basicConfig(level=logging.DEBUG)
CORS(application)

auth = HTTPBasicAuth(application)
db = SQLAlchemy(application)
bcrypt = Bcrypt(application)
ma = Marshmallow(application)
migrate = Migrate(application, db)
