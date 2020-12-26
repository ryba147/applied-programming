from announcements import db, ma


class User(db.Model):
    id = db.Column(db.Integer,nullable = False, primary_key=True)
    username = db.Column(db.String(64),unique=True)
    firstname = db.Column(db.String(64),nullable=False)
    lastname = db.Column(db.String(64),nullable=False)
    password = db.Column(db.String(64),nullable=False)
    location = db.Column(db.String(64),nullable=False)

    # def __repr__(self):
    #     return '<User {}>'.format(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.id)


class Announcement_type(db.Model):
    #__tablename__ = 'AnnouncementType'
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
    pub_date = db.Column(db.String(64),nullable=False)
    location = db.Column(db.String(64),nullable=False)
    announcement_type = db.Column(db.Integer,db.ForeignKey('announcement_type.id') ,nullable=False)
    def __repr__(self):
        return '<Announcement {}>'.format(self.id)
