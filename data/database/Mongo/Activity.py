import datetime

from mongoengine import StringField, ObjectIdField, EmbeddedDocument, EmbeddedDocumentField, IntField, ListField, \
    DecimalField, BooleanField, DateTimeField, FloatField
from data.database.database import mongo


class Address(EmbeddedDocument):
    longtitude = StringField(required=True)
    latitude = StringField(required=True)
    address = StringField(required=True)
    city_id = IntField(required=True)


class ActivityTicket(EmbeddedDocument):
    name = StringField(required=True)
    inventory = IntField(required=True)
    description = StringField(required=True)
    price = DecimalField(required=True, default=0.0)
    is_entity = BooleanField(required=True, default=True)


class ActivityCreator(EmbeddedDocument):
    name = StringField(required=True)
    pic = StringField(required=True)
    id = IntField(required=True)
    creator_type = IntField(required=True, default=1)  # 1=队列   2=主办方


class ActivityStatistics(EmbeddedDocument):
    attend_count = IntField(required=True, default=0)
    recommend_count = IntField(required=True, default=0)
    collect_count = IntField(required=True, default=0)
    comment_count = IntField(required=True, default=0)
    avg = FloatField(required=True, default=0.0)


class Activity(mongo.Document):
    title = StringField(max_length=100, required=True)
    address = EmbeddedDocumentField(Address, required=True)
    poster = StringField()
    pics = ListField(StringField)
    tickets = ListField(EmbeddedDocumentField(ActivityTicket))
    hx_group_id = StringField(max_length=18, required=True)
    labels = ListField(StringField(), required=True)
    begin_time = DateTimeField()
    end_time = DateTimeField()
    create_time = DateTimeField(required=True, default=datetime.datetime.now())
    # 队列活动开始时间
    queue_begin_time = ListField(DateTimeField)
    # 创建者信息
    creator_info = EmbeddedDocumentField(ActivityCreator, required=True)
    # 活动统计信息
    statistics = EmbeddedDocumentField(ActivityStatistics, required=True, default=ActivityStatistics())
    cast_much = StringField(default='')                                    # 消费金额
    is_free = BooleanField(required=True, default=False)           # 是否免费
    is_select = BooleanField(required=True, default=False)     # 是否精选
    is_recommend = BooleanField(required=True, default=False)  # 是否推荐
    is_passed = BooleanField(required=True, default=False)     # 是否审核
    meta = {
        'collection': 'activity',
        'indexes': [
            'labels',
            'begin_time',
            'end_time',
            'create_time'
        ]
    }