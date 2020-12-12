from announcements import application
from .schemas import *
from .models import *
from flask import jsonify, request


@application.route('/get', methods=['GET'])
def get_post():
    return jsonify({"Hello": "World"})


@application.route("/user", methods=['GET', 'POST'])
def user_method():
    if request.method == 'GET':
        all_users = User.query.all()
        return user_schemas.jsonify(all_users)
    else:
        username = request.json['username']
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        password = request.json['password']
        location = request.json['location']
        test_user = User(username=username, firstname=firstname, lastname=lastname, password=password,
                         location=location)
        user_data = user_schema.dump(test_user)
        try:
            UserSchema().load(user_data)
            db.session.add(test_user)
            db.session.commit()
            return user_schema.jsonify(test_user)

        except ValidationError as err:
            print("error")
            return jsonify(message=err.messages, status=405)  #


@application.route("/user/login/", methods=['GET'])
def login(username, password):
    user_username = User.query.get(username)
    user_password = User.query.get(password)
    return jsonify(StatusResponse().dump({"code": 200}))


@application.route("/user/<username>/", methods=['GET'])
def get_user(username):
    user_username = User.query.get(username)
    return user_schema.jsonify(user_username)


@application.route("/user/<username>/", methods=['PUT'])
def user_update(username):
    user_username = User.query.get(username)

    username = request.json['username']
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    location = request.json['location']

    user_username.username = username
    user_username.firstname = firstname
    user_username.lastname = lastname
    user_username.location = location

    db.session.commit()
    return user_schema.jsonify(user_username)


@application.route("/user/<username>/", methods=['DELETE'])
def delete_user(username):
    user_username = User.query.get(username)
    db.session.delete(user_username)
    db.session.commit()
    return user_schema.jsonify(user_username)

###############################################################################################################


@application.route("/announcementstype", methods=['POST'])
def announcement_type_post():
    id = request.json['id']
    description = request.json['description']
    test_post = AnnouncementType(id=id, description=description)
    test_data = announcement_type_schema.dump(test_post)
    AnnouncementTypeSchema.load(test_data)
    db.session.add(test_post)
    db.session.commit()
    return announcement_schema.jsonify(test_post)


@application.route("/announcements/", methods=['GET', 'POST'])
def announcement_method():
    if request.method == 'GET':
        all_announcements = Announcement.query.all()
        return announcement_schemas.jsonify(all_announcements)
    else:
        id = request.json['id']
        name = request.json['name']
        description = request.json['description']
        announcement_type = request.json['announcement_type']
        location = request.json['location']
        pub_date = request.json['pub_date']

        test_announcement = Announcement(id=id,name=name,
           description=description, announcement_type=announcement_type, location=location, pub_date=pub_date)

        announcement_data = announcement_schema.dump(test_announcement)
        try:
            UserSchema().load(announcement_data)
            db.session.add(test_announcement)
            db.session.commit()
            return announcement_schema.jsonify(test_announcement)

        except ValidationError as err:
            print("error")
            return jsonify(message=err.messages, status=405)  #


