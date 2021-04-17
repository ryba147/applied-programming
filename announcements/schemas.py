from .models import *
from marshmallow import Schema, fields, validate, ValidationError
from announcements import ma, db
from flask_bcrypt import generate_password_hash


class UserSchema(ma.Schema):
    id = fields.Integer(allow_none=True)
    username = fields.Str(validate=validate.Length(min=1, max=60))
    email = fields.Str(validate=validate.Length(min=1, max=60))
    firstname = fields.Str(validate=validate.Length(min=1, max=60))
    lastname = fields.Str(validate=validate.Length(min=1, max=60))
    password = fields.Str(validate=validate.Length(min=4, max=60))
    role = fields.Str()
    location = fields.Integer(allow_none=True)

    class Meta:
        model = User


user_schema = UserSchema()
user_schemas = UserSchema(many=True)


class AnnouncementTypeSchema(ma.Schema):
    id = fields.Integer(allow_none=True)
    description = fields.Str(validate=validate.Length(min=1, max=1024), allow_none=False)

    class Meta:
        model = AnnouncementType


announcement_type_schema = AnnouncementTypeSchema()
announcement_type_schemas = AnnouncementTypeSchema(many=True)


class AnnouncementSchema(ma.Schema):
    id = fields.Integer(allow_none=True)
    author_id = fields.Integer(required=False)
    name = fields.Str(validate=validate.Length(min=1, max=64))
    description = fields.Str(validate=validate.Length(min=1, max=500), required=False)
    img_name = fields.Str(allow_none=True)
    pub_date = fields.Str(allow_none=True)
    event_date = fields.Str(allow_none=True)
    location = fields.Integer(allow_none=True)
    type = fields.Integer(required=False)

    class Meta:
        model = Announcement


announcement_schema = AnnouncementSchema()
announcement_schemas = AnnouncementSchema(many=True)


class Location(ma.Schema):
    id = fields.Integer(allow_none=True)
    name = fields.Integer(allow_none=False)


location_schema = AnnouncementSchema()
location_schemas = AnnouncementSchema(many=True)


class StatusResponse(Schema):
    code = fields.Integer()
    type = fields.String(default="OK")
    message = fields.String(default="OK")
