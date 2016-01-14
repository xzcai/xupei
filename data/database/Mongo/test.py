from bson import objectid
from mongoengine import StringField

from src.extentions import mongo
from util.macro import code_send_mean


class Tes(mongo.Document):
    code = StringField(max_length=3, choices=code_send_mean)

    meta = {
        'collection': 'test3'
    }
