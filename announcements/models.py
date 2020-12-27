from announcements import db, ma


class User(db.Model):
    # __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    location = db.Column(db.Integer)

    # def __repr__(self):
    #     return '<User {}>'.format(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.id)


class Announcement_type(db.Model):
    # __tablename__ = 'announcementType'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    description = db.Column(db.String(64), nullable=False)

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
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    authorid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.String(64), nullable=False)
    location = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    announcement_type = db.Column(db.Integer, db.ForeignKey('announcement_type.id'), nullable=False)

    def __repr__(self):
        return '<Announcement {}>'.format(self.id)
