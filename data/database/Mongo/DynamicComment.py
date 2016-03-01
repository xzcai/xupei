import datetime

from mongoengine import IntField, EmbeddedDocument, ReferenceField, ListField, EmbeddedDocumentField, ObjectIdField, \
    StringField, Document

from data.database.Mongo.MongoUser import MongoUser
from data.database.database import mongo


class DynamicComment(Document):
    dynamic_id = ObjectIdField()
    add_time = mongo.DateTimeField(required=True, default=datetime.datetime.now())
    content = StringField()
    ori_user = ReferenceField(MongoUser)
    obj_user = ReferenceField(MongoUser)
    meta = {
        'collection': 'dynamic_comment',
        'indexes': [
            'dynamic_id'
        ]
    }

