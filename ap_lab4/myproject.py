from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand

application = Flask(__name__)

db = SQLAlchemy(application)

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab.db'
V = 3

migrate = Migrate(application, db)

class User(db.Model):
    #__tablename__ = 'User'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(64),nullable=False)
    lastname = db.Column(db.String(64),nullable=False)
    password = db.Column(db.String(64),nullable=False)
    location = db.Column(db.String(64),nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.id)

class AnnouncementType(db.Model):
    __tablename__ = 'AnnouncementType'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    description = db.Column(db.String(64),nullable=False)
    def __repr__(self):
        return '<AnnouncementType {}>'.format(self.id)


class Announcement(db.Model):
    #__tablename__ = 'Announcement'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    authorid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(64),nullable=False)
    description = db.Column(db.Text,nullable=False)
    pub_date = db.Column(db.String(11),nullable=False)
    location = db.Column(db.Integer,db.ForeignKey('location.id'),nullable=False)
    announcement_type = db.Column(db.Integer,db.ForeignKey('AnnouncementType.id') ,nullable=False)
    def __repr__(self):
        return '<Announcement {}>'.format(self.id)


class Location(db.Model):
    #__tablename__ = 'Location'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    def __repr__(self):
        return '<Location {}>'.format(self.id)





@application.route('/')
def index():
    return redirect(url_for('hello_world', url_v=v))


@application.route('/api/v1/hello-world-<int:url_v>')  # route() decorator tells Flask what URL should trigger our function
def hello_world(url_v):
    return render_template('hello.html', var=url_v)  # or return 'Hello World!'



if __name__ == '__main__':
    application.run()

