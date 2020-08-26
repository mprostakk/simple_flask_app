from backend.extension import db
from backend.models.task import Task, TaskSchema
from marshmallow import Schema, fields


class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    slack_api = db.StringField(required=True)
    tasks = db.EmbeddedDocumentListField(Task)


class UserSchema(Schema):
    id = fields.String(dump_only=True)
    username = fields.String()
    slack_api = fields.String()
    tasks = fields.List(fields.Nested(TaskSchema))


user_schema = UserSchema()
