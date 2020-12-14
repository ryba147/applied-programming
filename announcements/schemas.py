from .models import *
from marshmallow import Schema, fields, validate, ValidationError
from announcements import ma, db
from flask_bcrypt import generate_password_hash


class UserSchema(ma.Schema):
    id = fields.Integer(allow_none=True)
    username = fields.Str(validate=validate.Length(min=1, max=64))
    firstname = fields.Str(validate=validate.Length(min=1, max=64))
    lastname = fields.Str(validate=validate.Length(min=1, max=64))
    password = fields.password = fields.Function(
        deserialize=lambda obj: generate_password_hash(obj), load_only=True
    )
    location = fields.Integer()

    class Meta:
        model = User


user_schema = UserSchema()
user_schemas = UserSchema(many=True)


class AnnouncementTypeSchema(ma.Schema):
    id = fields.Integer(allow_none=True)
    description = fields.Str(validate=validate.Length(min=1, max=1024))

    class Meta:
        model = Announcement_type


announcement_type_schema = AnnouncementTypeSchema()
announcement_type_schemas = AnnouncementTypeSchema(many=True)


class AnnouncementSchema(ma.Schema):
    id = fields.Integer(unique=True)
    authorid = fields.Integer()
    name = fields.Str(validate=validate.Length(min=1, max=64))
    description = fields.Str(validate=validate.Length(min=1, max=64))
    pub_date = fields.Str(validate=validate.Length(min=1, max=12), allow_none=True)
    location = fields.Integer()
    announcement_type = fields.Integer()

    class Meta:
        model = Announcement


announcement_schema = AnnouncementSchema()
announcement_schemas = AnnouncementSchema(many=True)


class Location(ma.Schema):
    id = fields.Integer()
    name = fields.Integer()


class StatusResponse(Schema):
    code = fields.Integer()
    type = fields.String(default="OK")
    message = fields.String(default="OK")
