import os
import uuid

from sqlalchemy import and_
from werkzeug.utils import secure_filename

from announcements import application, db, auth, bcrypt, ALLOWED_EXTENSIONS
from .schemas import *
from .models import *
from flask import jsonify, request, abort, render_template
from marshmallow import ValidationError


@application.route('/')
def temp():
    return render_template('hello.html')


@auth.verify_password
def verify(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(401)
    # return user.password == password
    return bcrypt.check_password_hash(user.password, password)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route("/upload_file", methods=['POST'])
def upload_file():
    target = application.config['UPLOAD_FOLDER']
    if not os.path.isdir(target):
        os.mkdir(target)

    # check if the post request has the file part
    if 'file' not in request.files:
        # flash('No file part')
        return jsonify(message='No file part'), 404
    file = request.files['file']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        # flash('No selected file')
        return jsonify(message='No selected file'), 404

    if file and allowed_file(file.filename):
        file_extension = '.' + file.filename.rsplit('.', 1)[1].lower()
        upload_dest = '/'.join([target, str(uuid.uuid4())]) + file_extension
        file.save(os.path.join(upload_dest))
        return jsonify(message='Success'), 200


@application.route("/users", methods=['GET'])
def get_users():
    all_users = User.query.all()
    return user_schemas.jsonify(all_users)


@application.route("/users", methods=['POST'])
def post_user():
    username = request.json['username']
    if User.query.filter_by(username=username).first() is not None:
        return jsonify(message='User with the same name exists'), 403
    else:
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        email = request.json['email']
        password = request.json['password']
        role = request.json['role']
        # location = request.json['location']
        user = User(username=username, firstname=firstname, email=email, lastname=lastname, password=password,
                    role=role)
        user_data = user_schema.dump(user)
        try:
            UserSchema().load(user_data)
            h_query_pass = bcrypt.generate_password_hash(password)
            user = User(username=username, email=email, firstname=firstname, lastname=lastname,
                        password=h_query_pass,
                        role=role)
            db.session.add(user)
            db.session.commit()
            return user_schema.jsonify(user), 201
        except ValidationError as err:
            return jsonify(message=err.messages), 405


@application.route("/users/<username>", methods=['GET'])
def get_user(username):
    user_username = User.query.filter_by(username=username).first()
    if user_username is None:
        return jsonify(message='User not found'), 404
    return user_schema.jsonify(user_username)


@application.route("/users/logout", methods=['GET'])
@auth.login_required
def logout():
    return jsonify(message='Logout successful'), 200


@application.route("/users/login", methods=['GET'])
def login():
    q_username = request.args.get('username')
    q_pass = request.args.get('password')
    user = User.query.filter_by(username=q_username).first()
    if user is not None:
        if bcrypt.check_password_hash(user.password, q_pass):
            return user_schema.jsonify(user), 200
    return jsonify(message='Wrong username or password'), 404


@application.route("/users/<username>", methods=['PUT'])
@auth.login_required
def user_update(username):
    user_up = User.query.get(username)
    if user_up is None:
        abort(404, "User not found")
    try:
        user_up.username = request.json['username']
        user_up.firstname = request.json['firstname']
        user_up.lastname = request.json['lastname']
        user_up.location = request.json['location']
        password = request.json['password']
        if not bcrypt.check_password_hash(user_up.password, password):
            user_up.password = bcrypt.generate_password_hash(password)
        db.session.commit()
        return user_schema.jsonify(user_up)
    except ValidationError as err:
        return jsonify(message=err.messages), 405


@application.route("/users", methods=['DELETE'])
@auth.login_required
def delete_user():
    user = User.query.filter_by(username=request.args.get('username')).first()
    if user is None:
        return jsonify(message='user not found'), 404
    else:
        db.session.delete(user)
        db.session.commit()
        return user_schema.jsonify(user)


@application.route("/announcements", methods=['GET'])
def announcement_method():
    all_announcements = Announcement.query.all()
    return announcement_schemas.jsonify(all_announcements)


@application.route("/announcements", methods=['POST'])
@auth.login_required
def post_announcement():
    post_id = request.json['id']
    author_id = request.json['author_id']
    name = request.json['name']
    description = request.json['description']
    location = request.json['location']
    announcement_type = request.json['announcement_type']

    test_announcement = Announcement(id=post_id, author_id=author_id, name=name,
                                     description=description, location=location,
                                     type=announcement_type)
    announcement_data = announcement_schema.dump(test_announcement)
    try:
        AnnouncementSchema().load(announcement_data)
        db.session.add(test_announcement)
        db.session.commit()
        return announcement_schema.jsonify(test_announcement)
    except ValidationError as err:
        return jsonify(message=err.messages), 405


@application.route("/announcements/nearby", methods=['GET'])
@auth.login_required
def get_nearby_announcement():
    query_location = request.args.get('location')
    application.logger.info(query_location)
    if query_location is not None:
        nearby_announcements = Announcement.query \
            .join(Location, Announcement.id == Location.id) \
            .filter(and_(Announcement.type == 1, Location.name == query_location))
    else:
        nearby_announcements = Announcement.query.filter_by(announcement_type=1).all()
    # application.logger.info(nearby_announcements)
    return announcement_schemas.jsonify(nearby_announcements)


@application.route("/announcements/<int:announcement_id>/", methods=['GET'])
def get_announcement(announcement_id):
    announcement_by_id = Announcement.query.get(announcement_id)
    if announcement_by_id is None:
        return jsonify(message='announcement is not found'), 404
    return announcement_schema.jsonify(announcement_by_id)


@application.route("/announcements/<announcement>/", methods=['PUT'])
@auth.login_required
def announcement_update(announcement):
    announcement = Announcement.query.get(announcement)
    if announcement is None:
        return jsonify(message='Announcement not found'), 404
    try:
        announcement.author_id = request.json['author_id']
        announcement.title = request.json['name']
        announcement.location = request.json['location']
        announcement.type_name = request.json['description']
        announcement.pub_date = request.json['pub_date']
        announcement.type = request.json['announcement_type']
        db.session.commit()
        return announcement_schema.jsonify(announcement)
    except ValidationError as err:
        return jsonify(message=err.messages), 405


@application.route("/announcements/<int:announcement_id>/", methods=['DELETE'])
@auth.login_required
def delete_announcement(announcement_id):
    announcement = Announcement.query.get(announcement_id)
    if announcement is None:
        return jsonify(message='Announcement not found'), 404
    db.session.delete(announcement)
    db.session.commit()
    return announcement_schema.jsonify(announcement)
