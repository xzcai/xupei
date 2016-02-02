from mongoengine import StringField, IntField
from data.database.database import mongo


class City(mongo.Document):
    id=IntField(primary_key=True)
    code = StringField()
    city = StringField(max_length=100)
    province = StringField()
    meta = {
        'collection': 'city'
    }
