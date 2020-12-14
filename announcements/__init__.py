from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, MigrateCommand
from flask_bcrypt import Bcrypt

application = Flask(__name__)


application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../lab.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

ma = Marshmallow(application)
migrate = Migrate(application, db)
bcrypt = Bcrypt(application)