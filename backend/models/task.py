from backend.extension import db
import datetime
from marshmallow import Schema, fields
from bson.objectid import ObjectId


class Task(db.EmbeddedDocument):
    _id = db.ObjectIdField(required=True, default=lambda: ObjectId())

    name = db.StringField(required=True)
    message = db.StringField()
    date_created = db.DateTimeField(default=datetime.datetime.utcnow)
    date_schedule = db.DateTimeField()
    notified = db.BooleanField(default=False)


class TaskSchema(Schema):
    _id = fields.String(dump_only=True)
    name = fields.String()
    message = fields.String()
    date_created = fields.DateTime(dump_only=True)
    date_schedule = fields.DateTime()


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
