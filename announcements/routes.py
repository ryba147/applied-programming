from announcements import application, bcrypt
from .schemas import *
from .models import *
from flask import jsonify, request


@application.route("/user", methods=['GET', 'POST'])
def user_method():
    if request.method == 'GET':
        all_users = User.query.all()
        return user_schemas.jsonify(all_users)
    else:
        query_username = request.args.get('username')
        if User.query.filter_by(username=query_username).first() is not None:
            return jsonify(message='user with this name exists', status=403)
        else:
            id = request.json['id']
            username = request.json['username']
            firstname = request.json['firstname']
            lastname = request.json['lastname']
            password = request.json['password']
            location = request.json['location']
            test_user = User(id=id, username=username, firstname=firstname, lastname=lastname, password=password,
                             location=location)
            user_data = user_schema.dump(test_user)
            try:
                UserSchema().load(user_data)
                h_query_pass = bcrypt.generate_password_hash(password)
                test_user = User(id=id, username=username, firstname=firstname, lastname=lastname, password=h_query_pass,
                                 location=location)
                db.session.add(test_user)
                db.session.commit()
                return user_schema.jsonify(test_user)

            except ValidationError as err:
                print("error")
                return jsonify(message=err.messages, status=405)


@application.route("/user/<username>/", methods=['GET'])
def get_user(username):
    user_username = User.query.get(username)
    if user_username is None:
        return jsonify(message='user not found', status=404)
    return user_schema.jsonify(user_username)


@application.route("/user/logout/", methods=['GET'])
def logout():
    return "You are log out"


@application.route("/user/login/", methods=['GET'])
def login():
    query_username = request.args.get('username')
    query_pass = request.args.get('password')
    u = User.query.filter_by(username=query_username).first()
    if u is not None:
        return jsonify(message='OK', status=200)
    return jsonify(message='wrong username or password', status=403)


@application.route("/user/<username>/", methods=['PUT'])
def user_update(username):
    user_up = User.query.get(username)
    if user_up is None:
        return jsonify(message='user not found', status=404)
    try:
        user_up.username = request.json['username']
        user_up.firstname = request.json['firstname']
        user_up.lastname = request.json['lastname']
        user_up.location = request.json['location']
        password = request.json['password']
        if not bcrypt.check_password_hash(user_up.password, password):
            print("password was changed")
            user_up.password = bcrypt.generate_password_hash(password)
        db.session.commit()
        return user_schema.jsonify(user_up)
    except ValidationError as err:
        return jsonify(message=err.messages, status=405)


@application.route("/user/<username>/", methods=['DELETE'])
def delete_user(username):
    user_username = User.query.get(username)
    if user_username is None:
        return jsonify(message='user not found', status=404)
    db.session.delete(user_username)
    db.session.commit()
    return user_schema.jsonify(user_username)

###############################################################################################################


@application.route("/announcement/", methods=['GET', 'POST'])
def announcement_method():
    if request.method == 'GET':
        all_announcements = Announcement.query.all()
        return announcement_schemas.jsonify(all_announcements)
    else:
        id = request.json['id']
        authorid = request.json['authorid']
        name = request.json['name']
        description = request.json['description']
        pub_date = request.json['pub_date']
        location = request.json['location']
        announcement_type = request.json['announcement_type']

        test_announcement = Announcement(id=id, authorid=authorid, name=name,
           description=description, pub_date=pub_date, location=location, announcement_type=announcement_type)
        announcement_data = announcement_schema.dump(test_announcement)
        try:
            AnnouncementSchema().load(announcement_data)
            db.session.add(test_announcement)
            db.session.commit()
            return announcement_schema.jsonify(test_announcement)

        except ValidationError as err:
            return jsonify(message=err.messages, status=405)


@application.route("/announcement/nearby/", methods=['GET'])
def get_nearby_announcement():
    all_announcements_by_location = Announcement.query.filter_by(announcement_type='1').all()
    return announcement_schemas.jsonify(all_announcements_by_location)


@application.route("/announcement/<int:announcement_id>/", methods=['GET'])
def get_announcement(announcement_id):
    announcement_by_id = Announcement.query.get(announcement_id)
    if announcement_by_id is None:
        return jsonify(message='announcement is not found', status=404)
    return announcement_schema.jsonify(announcement_by_id)


@application.route("/announcement/<int:announcement_id>/", methods=['PUT'])
def announcement_update(announcement_id):
    announcement_id = Announcement.query.get(announcement_id)
    if announcement_id is None:
        return jsonify(message='announcement is not found', status=404)
    try:
        announcement_id.authorid = request.json['authorid']
        announcement_id.name = request.json['name']
        announcement_id.location = request.json['location']
        announcement_id.description = request.json['description']
        announcement_id.pub_date = request.json['pub_date']
        announcement_id.announcement_type = request.json['announcement_type']

        db.session.commit()
        return announcement_schema.jsonify(announcement_id)
    except ValidationError as err:
        return jsonify(message=err.messages, status=405)


@application.route("/announcement/<int:announcement_id>/", methods=['DELETE'])
def delete_announcement(announcement_id):
    announcement_by_id = Announcement.query.get(announcement_id)
    if announcement_by_id is None:
        return jsonify(message='announcement is not found', status=404)
    db.session.delete(announcement_by_id)
    db.session.commit()
    return announcement_schema.jsonify(announcement_by_id)

