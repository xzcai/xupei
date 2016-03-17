from mongoengine import StringField, ListField, IntField, ReferenceField, ObjectIdField, EmbeddedDocumentField, \
    EmbeddedDocument, BooleanField, Document

from data.database.Mongo.Activity import Activity
# from data.database.Mongo.DynamicComment import DynamicComment
from data.database.database import mongo
import datetime


class Token(EmbeddedDocument):
    value = StringField(default='')
    due_time = mongo.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(seconds=24 * 60 * 60 * 60))


class Info(EmbeddedDocument):
    xp_account = StringField()
    pic = StringField(required=True)
    nickname = StringField(required=True)
    signature = StringField(default='')
    sex = BooleanField(default=False)  # false=男
    province = StringField(default='')
    city = StringField(default='')
    user_origin = IntField(default=1)
    device_id = StringField(default='')
    hx_account = StringField(required=True)
    hx_password = StringField(required=True)
    is_verify = BooleanField(default=False)
    is_protect = BooleanField(default=False)


class Interrupt(EmbeddedDocument):
    add_time = mongo.DateTimeField(default=datetime.datetime.now())
    content = StringField()
    user_id = ReferenceField('MongoUser') #IntField()


# class Posture(EmbeddedDocument):
#     time = mongo.DateTimeField(default=datetime.datetime.now())
#     content = StringField()
#     pic = StringField()


class ActivityState(EmbeddedDocument):
    object_id = ObjectIdField()
    active_type = IntField(choices=((1, '推荐'), (2, '参加'), (3, '发布'), (4, '动态'), (5, '姿态')))
    interrupt = EmbeddedDocumentField(Interrupt)
    content = StringField()
    # posture = ListField(EmbeddedDocumentField(Posture))
    raise_up = ListField(ReferenceField('MongoUser'))  # ListField(IntField(), default=list)

    address = StringField()
    pics = ListField(StringField(), default=list)
    longitude = StringField()
    latitude = StringField()
    # 活动态添加时间
    add_time = mongo.DateTimeField(required=True, default=datetime.datetime.now())
    # 个人发布活动开始时间
    begin_time = StringField()
    # 推荐 参加 活动id
    activity = ReferenceField(Activity)
    # 是否城市可见
    city_id = IntField(required=True)
    # 是否好友可见
    is_friend = BooleanField(default=False)


class ActivityNum(EmbeddedDocument):
    interrupt_num = IntField(required=True, default=0)
    raise_num = IntField(required=True, default=0)
    attend_num = IntField(required=True, default=0)
    comment_num = IntField(required=True, default=0)


class MessageInfo(EmbeddedDocument):
    user = ReferenceField('MongoUser')
    add_time = mongo.DateTimeField(required=True, default=datetime.datetime.now())
    type = IntField(choices=(1, 2, 3, 4, 5))  # 1= 插话；2=点赞；3=参加；4=评论


class MongoUser(Document):
    mysql_id = IntField(primary_key=True)
    token = EmbeddedDocumentField(Token)
    friends = ListField(IntField(), default=list)
    activity_recommend = ListField(ObjectIdField(), default=list)
    activity_attend = ListField(ObjectIdField(), default=list)
    activity_collect = ListField(ObjectIdField(), default=list)
    info = EmbeddedDocumentField(Info, required=True)
    activity_state = ListField(EmbeddedDocumentField(ActivityState), default=list)
    message_info = ListField(EmbeddedDocumentField(MessageInfo))
    meta = {
        'collection': 'user_info',
        'indexes': [
            'info.hx_account',
            'activity_state.object_id',
            'activity_state.add_time'
        ]
    }
