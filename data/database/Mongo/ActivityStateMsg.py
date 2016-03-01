import datetime

from mongoengine import IntField, EmbeddedDocument, ReferenceField, ListField, EmbeddedDocumentField

from data.database.Mongo import MongoUser
from data.database.database import mongo

#  数组里面不能引用

class ActivityStateNum(EmbeddedDocument):
    # user = ReferenceField(MongoUser)
    add_time = mongo.DateTimeField(required=True, default=datetime.datetime.now())
    op_type = IntField()


class ActivityStateMsg(mongo.Document):
    mysql_id = IntField(primary_key=True)
    msg_info = ListField(EmbeddedDocumentField(ActivityStateNum),default=list)
