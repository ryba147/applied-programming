import base64
import os
import uuid

from cloudinary.uploader import upload
from flask import jsonify, request, abort, render_template, make_response
from pip._vendor import requests
from sqlalchemy import and_, null

from announcements import application, auth, bcrypt, ALLOWED_EXTENSIONS, APP_ROOT
from .schemas import *


@application.route('/')
def temp():
    return render_template('hello.html')


@auth.verify_password
def verify(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(401)
    return bcrypt.check_password_hash(user.password, password)


def generate_basic_auth_header(username, password):
    return base64.b64encode(
        '{username}:{password}'.format(
            username=username,
            password=password).encode()
    ).decode()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @application.route("/upload_file", methods=['POST'])
def upload_file(upload_type):
    if 'file' not in request.files:
        return None
    file = request.files['file']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return None

    if file and allowed_file(file.filename):
        # using Cloudinary API
        if upload_type == 'to_cloud':
            upload_result = upload(file)
            # return jsonify(cloudinary_url(upload_result['secure_url'])), 200
            return upload_result['public_id']

        if upload_type == 'locally':
            target = os.path.join(APP_ROOT, application.config['UPLOAD_FOLDER'])
            if not os.path.isdir(target):
                os.mkdir(target)
            file_extension = '.' + file.filename.rsplit('.', 1)[1].lower()
            unique_filename = str(uuid.uuid4()) + file_extension
            file_dest = '/'.join([target, unique_filename])
            file.save(os.path.join(file_dest))
            print(os.path.join(file_dest))

            return unique_filename


@application.route("/users", methods=['GET'])
@auth.login_required
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
        email = requests.utils.unquote(request.json['email'])
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


@application.route("/users/<int:user_id>", methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify(message='User not found'), 404
    return user_schema.jsonify(user), 200


@application.route("/users/<username>", methods=['GET'])
def get_user_by_uname(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify(message='User not found'), 404
    return user_schema.jsonify(user), 200


@application.route("/users/logout", methods=['GET'])
@auth.login_required
def logout():
    return jsonify(message='Logout successful'), 200


@application.route("/users/login", methods=['GET'])
def login():
    q_username = request.args.get('username')
    q_pass = request.args.get('password')
    user = User.query.filter_by(username=q_username).first()
    # .join(Location, Location.id == User.location)

    print(user)

    if user is not None:
        user_data = user_schema.dump(user)
        if bcrypt.check_password_hash(user.password, q_pass):
            response = make_response(
                jsonify(
                    {"userData": UserSchema().load(user_data),
                     "authHeader": generate_basic_auth_header(q_username, q_pass)}
                ), 200
            )
            response.headers["Content-Type"] = "application/json"
            return response
    return jsonify(message='Wrong username or password'), 404


@application.route("/users/<int:user_id>", methods=['PUT'])
@auth.login_required
def user_update(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404, "User not found")
    try:
        user.firstname = request.form['firstname']
        user.lastname = request.form['lastname']
        user.email = requests.utils.unquote(request.form['email'])

        if request.form['location'].strip():
            user.location = int(request.form['location'])

        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        if password.strip():
            if password != confirm_password:
                raise ValidationError
            if not bcrypt.check_password_hash(user.password, password):
                user.password = bcrypt.generate_password_hash(password)
        if request.files:
            user.img_name = upload_file('to_cloud')
        db.session.commit()
        # return user_schema.jsonify(user)
        user_data = user_schema.dump(user)

        response = make_response(
            jsonify(
                {"userData": UserSchema().load(user_data),
                 "authHeader": generate_basic_auth_header(user.username, password)}
            ), 200
        )
        response.headers["Content-Type"] = "application/json"
        return response
    except ValidationError as err:
        return jsonify(message=err.messages), 405


@application.route("/users/<int:id>", methods=['DELETE'])
@auth.login_required
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return jsonify(message='User not found'), 404
    else:
        db.session.delete(user)
        db.session.commit()
        return user_schema.jsonify(user)


@application.route("/announcements", methods=['GET'])
def get_announcements():
    all_announcements = Announcement.query.all()
    return announcement_schemas.jsonify(all_announcements)


@application.route("/announcements", methods=['POST'])
@auth.login_required
def post_announcement():
    author_id = request.form['author_id']
    title = request.form['title']
    description = request.form['description']
    img_name = upload_file('to_cloud')
    announcement_type = request.form['announcement_type']
    event_date = request.form['event_date']
    location = request.form['location']

    test_announcement = Announcement(author_id=author_id,
                                     title=title,
                                     pub_date=str(datetime.now().isoformat()),
                                     event_date=event_date,
                                     description=description,
                                     img_name=img_name,
                                     location=location,
                                     type=announcement_type)
    announcement_data = announcement_schema.dump(test_announcement)
    try:
        AnnouncementSchema().load(announcement_data)
        db.session.add(test_announcement)
        db.session.commit()
        return announcement_schema.jsonify(test_announcement), 201
    except ValidationError as err:
        return jsonify(message=err.messages), 405


@application.route("/announcements/filter_by", methods=['GET'])
@auth.login_required
def get_nearby_announcement():
    q_location = request.args.get('location')
    q_author_id = request.args.get('author_id')

    if q_author_id is not None:
        application.logger.info(q_author_id)
        nearby_announcements = Announcement.query.filter_by(author_id=q_author_id)
        return announcement_schemas.jsonify(nearby_announcements)

    if q_location is not None:
        application.logger.info(q_location)
        nearby_announcements = Announcement.query \
            .join(Location, Announcement.id == Location.id) \
            .filter(and_(Announcement.type == 1, Location.name == q_location))
        return announcement_schemas.jsonify(nearby_announcements)

    return jsonify(message='not_found'), 404


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
