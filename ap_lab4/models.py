from app import db

class User(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(64),nullable=False)
    lastname = db.Column(db.String(64),nullable=False)
    password = db.Column(db.String(64),nullable=False)
    location = db.Column(db.String(64),nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.id)

class Location(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    def __repr__(self):
        return '<Location {}>'.format(self.id)

class AnnouncementType(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    description = db.Column(db.String(64),nullable=False)
    def __repr__(self):
        return '<AnnouncementType {}>'.format(self.id)

class Announcement(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    authorid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(64),nullable=False)
    description = db.Column(db.Text,nullable=False)
    pub_date = db.Column(db.String(11),nullable=False)
    location = db.Column(db.Integer,db.ForeignKey('Location.id'),nullable=False)
    announcement_type = db.Column(db.Integer,db.ForeignKey('AnnouncementType.id') ,nullable=False)
    def __repr__(self):
        return '<Announcement {}>'.format(self.id)

#session = db.relationship('Session', cascade="all, delete", backref=db.backref('film', lazy=True))
#session = db.Column(db.Array, db.ForeignKey('session', ondelete="cascade"), nullable=False, unique=True)
