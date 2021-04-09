from datetime import datetime

from announcements import db, ma


class User(db.Model):
    # __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)  # 60
    firstname = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(40), default="Regular", nullable=False)
    location = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class AnnouncementType(db.Model):
    # __tablename__ = 'announcementType'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    type_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<AnnouncementType {}>'.format(self.id)


class Location(db.Model):
    # __tablename__ = 'Location'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return '<Location {}>'.format(self.id)


class Announcement(db.Model):
    # __tablename__ = 'Announcement'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.String(64), default=datetime.now(), nullable=True)
    location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)
    announcement_type = db.Column(db.Integer, db.ForeignKey('announcement_type.id'), nullable=False)

    def __repr__(self):
        return '<Announcement {}>'.format(self.name)
