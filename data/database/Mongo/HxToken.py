
from mongoengine import StringField
from data.database.database import mongo


class HxToken(mongo.Document):
    value = StringField(max_length=50)
    past_due = mongo.DateTimeField()

