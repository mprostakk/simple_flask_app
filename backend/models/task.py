from backend.extension import db
import datetime
from marshmallow import Schema, fields


class Task(db.EmbeddedDocument):
    name = db.StringField(required=True)
    message = db.StringField()
    date_created = db.DateTimeField(default=datetime.datetime.utcnow)
    date_schedule = db.DateTimeField()
    notified = db.BooleanField(default=False)


class TaskSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String()
    message = fields.String()
    date_created = fields.DateTime(dump_only=True)
    date_schedule = fields.DateTime()


task_schema = TaskSchema()
