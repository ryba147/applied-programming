from announcements import application, db, auth, bcrypt
from .schemas import *
from .models import *
from flask import jsonify, request, abort
import base64

@auth.verify_password
def verify(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(401)
    return bcrypt.check_password_hash(user.password, password)


@application.route("/user", methods=['GET'])
def get_users():
    all_users = User.query.all()
    return user_schemas.jsonify(all_users)


@application.route("/user/", methods=['POST'])
def post_user():
    query_username = request.args.get('username')
    if User.query.filter_by(username=query_username).first() is not None:
        abort(403, "User with that name exists!!!")
    username = request.form['username']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    password = request.form['password']
    location = request.form['location']
    test_user = User(username=username, firstname=firstname, lastname=lastname, password=password,
                         location=location)
    user_data = user_schema.dump(test_user)
    try:
        UserSchema().load(user_data)
        h_query_pass = bcrypt.generate_password_hash(password).decode()
        test_user = User(username=username, firstname=firstname, lastname=lastname,
                                 password=h_query_pass,
                                 location=location)
        db.session.add(test_user)
        db.session.commit()
        return user_schema.jsonify(test_user)
    except ValidationError as err:
        abort(405,err.messages)


@application.route("/user/<string:username>", methods=['GET'])
def get_user(username):
    user_username = User.query.filter_by(username=username).first()
    if user_username is None:
        abort(404,'user not found')
    return user_schema.jsonify(user_username)


@application.route("/user/logout/", methods=['GET'])
@auth.login_required
def logout():
    return "You are log out"


@application.route("/user/login/", methods=['GET'])
def login():
    query_username = request.args.get('username')
    query_pass = request.args.get('password')
    user = User.query.filter_by(username=query_username).first()
    if user is not None:
        return 'Ok'
    return 'Wrong username or password',403


@application.route("/user/<string:username>/", methods=['PUT'])
@auth.login_required
def user_update(username):
    user_up = User.query.get(username)
    if user_up is None:
        abort(404,'User not found')
    try:
        user_up.username = request.form['username']
        user_up.firstname = request.form['firstname']
        user_up.lastname = request.form['lastname']
        user_up.location = request.form['location']
        password = request.form['password']
        print(user_up.password)
        print(bcrypt.generate_password_hash(password))
        if not bcrypt.check_password_hash(user_up.password, password):
            user_up.password = bcrypt.generate_password_hash(password)
        db.session.commit()
        return user_schema.jsonify(user_up)
    except ValidationError as err:
        abort(405,err.messages)


@application.route("/user/<string:username>/", methods=['DELETE'])
@auth.login_required
def delete_user(username):
    user_username = User.query.filter_by(username = username).first()
    if user_username is None:
        abort(404,'user not found')
    db.session.delete(user_username)
    db.session.commit()
  #  returned = user_schema.jsonify(user_username)
    return user_schema.jsonify(user_username)


###############################################################################################################


@application.route("/announcement/", methods=['GET'])
def announcement_method():
    all_announcements = Announcement.query.all()
    return announcement_schemas.jsonify(all_announcements)


@application.route("/announcement/", methods=['POST'])
@auth.login_required
def post_announcement():
    post_id = request.form['id']
    authorid = request.form['authorid']
    name = request.form['name']
    description = request.form['description']
    pub_date = request.form['pub_date']
    location = request.form['location']
    announcement_type = request.form['announcement_type']

    test_announcement = Announcement(id=post_id, authorid=authorid, name=name,
                                     description=description, pub_date=pub_date, location=location,
                                     announcement_type=announcement_type)
    announcement_data = announcement_schema.dump(test_announcement)
    try:
        AnnouncementSchema().load(announcement_data)
        db.session.add(test_announcement)
        db.session.commit()
        return announcement_schema.jsonify(test_announcement)
    except ValidationError as err:
        return jsonify(message=err.messages, status=405)


@application.route("/announcement/nearby/<int:userLocation>", methods=['GET'])
def get_nearby_announcement(userLocation):
    all_announcements_by_location = Announcement.query.filter_by(location=userLocation).all()
    return announcement_schemas.jsonify(all_announcements_by_location)


@application.route("/announcement/<int:announcement_id>/", methods=['GET'])
def get_announcement(announcement_id):
    announcement_by_id = Announcement.query.filter_by(id = announcement_id).first()
    if announcement_by_id is None:
        abort(404,"announcement not found")
    return announcement_schema.jsonify(announcement_by_id)


@application.route("/announcement/<int:announcement_id>/", methods=['PUT'])
@auth.login_required
def announcement_update(announcement_id):
    announcementToUpdate = Announcement.query.filter_by(id=announcement_id).first()
    if announcement_id is None:
        return jsonify(message='announcement is not found', status=404)
    try:
        announcementToUpdate.authorid = request.form['authorid']
        announcementToUpdate.name = request.form['name']
        announcementToUpdate.location = request.form['location']
        announcementToUpdate.description = request.form['description']
        announcementToUpdate.pub_date = request.form['pub_date']
        announcementToUpdate.announcement_type = request.form['announcement_type']
        db.session.commit()
        return announcement_schema.jsonify(announcement_id)
    except ValidationError as err:

        return jsonify(message=err.messages, status=405)


@application.route("/announcement/<int:announcement_id>/", methods=['DELETE'])
@auth.login_required
def delete_announcement(announcement_id):
    announcement_by_id = Announcement.query.filter_by(id=announcement_id).first()
    if announcement_by_id is None:
        abort(404,'announcement not found')
    db.session.delete(announcement_by_id)
    db.session.commit()
    return announcement_schema.jsonify(announcement_by_id)
