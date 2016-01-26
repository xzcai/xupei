import datetime

from mongoengine import StringField, IntField, BooleanField
from data.database.database import mongo


class PhoneDynamicCode(mongo.Document):
    phone = StringField(max_length=11)
    send_time = mongo.DateTimeField(default=datetime.datetime.now())
    send_code = IntField(required=True)
    send_count = IntField(default=1)
    # is_used = BooleanField(default=False)
    send_type = IntField(default=1)
    meta = {
        'collection': 'phone_dynamic_code'
    }
