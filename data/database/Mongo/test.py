from mongoengine import StringField, IntField, ListField, EmbeddedDocumentField, EmbeddedDocument

from data.database.database import mongo
from util.macro import code_send_mean


class TestData(EmbeddedDocument):
    num = IntField()
    str_data = StringField()


class Tes(mongo.Document):
    code = StringField()
    name = StringField()
    age = IntField()
    arr_list = ListField(EmbeddedDocumentField(TestData), default=list)
    meta = {
        'collection': 'test3'
    }
