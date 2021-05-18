import logging
import os

import cloudinary
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send

# 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

application = Flask(__name__, template_folder='../templates')

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../lab.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = 'very-secret-key'
application.config['UPLOAD_FOLDER'] = '../uploaded_media'
application.config['CLOUDINARY_URL'] = 'http://res.cloudinary.com/htmpcvv0s/image/upload/'
cloudinary.config(
    cloud_name="htmpcvv0s",
    api_key="236736167834651",
    api_secret="tuPf9BGerOvRg0eOuScG3ZeESUQ"
)
logging.basicConfig(level=logging.DEBUG)
CORS(application)

auth = HTTPBasicAuth(application)
db = SQLAlchemy(application)
bcrypt = Bcrypt(application)
ma = Marshmallow(application)
migrate = Migrate(application, db)
socketio = SocketIO(application, cors_allowed_origins='*')
