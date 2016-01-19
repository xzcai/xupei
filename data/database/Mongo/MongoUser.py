from mongoengine import StringField, ListField, IntField, ReferenceField, ObjectIdField, EmbeddedDocumentField, \
    EmbeddedDocument
from data.database.database import mongo
import datetime

from util.macro import code_send_mean, active_state_type


class Token(EmbeddedDocument):
    value = StringField()
    due_time = mongo.DateTimeField()


class Info(EmbeddedDocument):
    pic = StringField()
    nickname = StringField()


class Verify(EmbeddedDocument):
    phone = StringField(max_length=11, min_length=11)
    count = IntField()
    due_time = mongo.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(10 * 60))
    type = IntField(choices=code_send_mean)


class InterruptComment(EmbeddedDocument):
    time = mongo.DateTimeField(default=datetime.datetime.now())
    content = StringField()
    user_id = IntField()


class Posture(EmbeddedDocument):
    time = mongo.DateTimeField(default=datetime.datetime.now())
    content = StringField()
    pic = StringField()


class ActivityState(EmbeddedDocument):
    type = IntField(choices=active_state_type)
    interrupt_comment = EmbeddedDocumentField(InterruptComment)
    content = StringField()
    posture = EmbeddedDocumentField(Posture)
    raise_up = ListField(IntField(), default=list)
    address = StringField()
    pics = ListField(StringField(), default=list)
    longitude = StringField()
    latitude = StringField()


class MongoUser(mongo.Document):
    mysql_id = IntField(primary_key=True)
    token = EmbeddedDocumentField(Token)
    friends = ListField(IntField(), default=list)
    activity_recommend = ListField(ObjectIdField(), default=list)
    activity_attend = ListField(ObjectIdField(), default=list)
    info = EmbeddedDocumentField(Info)
    verify = EmbeddedDocumentField(Verify)
    activity_state = ListField(EmbeddedDocumentField(ActivityState), default=list)

    meta = {
        'collection': 'user_info'
    }
