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
@application.route("/announcements/", methods=['GET', 'POST'])
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
            print("error")
            return jsonify(message=err.messages, status=405)  #


@application.route("/announcement/<announcementId>/", methods=['PUT'])
def user_update(announcementId):
    announcement_id = User.query.get(announcementId)
    authorid = request.json['authorid']
    name = request.json['name']
    description = request.json['description']
    pub_date = request.json['pub_date']
    location = request.json['location']
    announcement_type = request.json['announcement_type']

    announcement_id.authorid = request.json['authorid']
    announcement_id.name = name
    announcement_id.location = location
    announcement_id.description = description
    announcement_id.pub_date = pub_date
    announcement_id.announcement_type = announcement_type

    db.session.commit()
    return announcement_schema.jsonify(announcement_id)

