import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from myproject import application, db


application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab.db'

migrate = Migrate(application, db)
manager = Manager(application)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()