from .models import *
from marshmallow import Schema, fields, validate, ValidationError
from announcements import ma, db


class UserSchema(ma.Schema):
    id = fields.Integer(allow_none=True)
    username = fields.Str(validate=validate.Length(min=5, max=60), allow_none=True)
    email = fields.Str(validate=validate.Length(min=5, max=60), allow_none=True)
    firstname = fields.Str(validate=validate.Length(min=3, max=60), allow_none=True)
    lastname = fields.Str(validate=validate.Length(min=3, max=60), allow_none=True)
    img_name = fields.Str(allow_none=True)
    password = fields.Str(validate=validate.Length(min=5, max=60), allow_none=True)
    role = fields.Str(allow_none=True)
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
    author_id = fields.Integer(allow_none=True)
    title = fields.Str(validate=validate.Length(min=0, max=64), allow_none=True)
    description = fields.Str(validate=validate.Length(min=0, max=500), allow_none=True)
    img_name = fields.Str(allow_none=True)
    pub_date = fields.Str(allow_none=True)
    event_date = fields.Str(allow_none=True)
    location = fields.Integer(allow_none=True)
    type = fields.Integer(allow_none=True)

    class Meta:
        model = Announcement


announcement_schema = AnnouncementSchema()
announcement_schemas = AnnouncementSchema(many=True)


class LocationSchema(ma.Schema):
    id = fields.Integer(allow_none=True)
    name = fields.Integer(allow_none=False)

    class Meta:
        model = Location


location_schema = LocationSchema()
location_schemas = LocationSchema(many=True)


class StatusResponse(Schema):
    code = fields.Integer()
    type = fields.String(default="OK")
    message = fields.String(default="OK")
