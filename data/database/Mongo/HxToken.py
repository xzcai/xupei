
from mongoengine import StringField
from data.database.database import mongo


class HxToken(mongo.Document):
    value = StringField(max_length=100)
    past_due = mongo.DateTimeField()

    meta = {
        'collection': 'hx_token'
    }

