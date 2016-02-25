from mongoengine import StringField, ListField, IntField, ReferenceField, ObjectIdField, EmbeddedDocumentField, \
    EmbeddedDocument, BooleanField
from data.database.database import mongo
import datetime

from util.macro import code_send_mean, active_state_type


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


class InterruptComment(EmbeddedDocument):
    time = mongo.DateTimeField(default=datetime.datetime.now())
    content = StringField()
    user_id = IntField()


# class Posture(EmbeddedDocument):
#     time = mongo.DateTimeField(default=datetime.datetime.now())
#     content = StringField()
#     pic = StringField()


class ActivityState(EmbeddedDocument):
    object_id = ObjectIdField()
    active_type = IntField(choices=active_state_type)
    interrupt_comment = EmbeddedDocumentField(InterruptComment)
    content = StringField()
    # posture = ListField(EmbeddedDocumentField(Posture))
    raise_up = ListField(IntField(), default=list)
    address = StringField()
    pics = ListField(StringField(), default=list)
    longitude = StringField()
    latitude = StringField()
    # 活动态添加时间
    add_time = mongo.DateTimeField(required=True, default=datetime.datetime.now())
    # 个人发布活动开始时间
    begin_time = StringField()
    # 推荐 参加 活动id
    activity_id = ObjectIdField()
    # 是否城市可见
    is_city = BooleanField(default=False)
    # 是否好友可见
    is_friend = BooleanField(default=False)


class ActivityNum(EmbeddedDocument):
    interrupt_num = IntField(required=True, default=0)
    raise_num = IntField(required=True, default=0)
    attend_num = IntField(required=True, default=0)
    comment_num = IntField(required=True, default=0)


class MongoUser(mongo.Document):
    mysql_id = IntField(primary_key=True)
    token = EmbeddedDocumentField(Token)
    friends = ListField(IntField(), default=list)
    activity_recommend = ListField(ObjectIdField(), default=list)
    activity_attend = ListField(ObjectIdField(), default=list)
    activity_collect = ListField(ObjectIdField(), default=list)
    info = EmbeddedDocumentField(Info, required=True)
    activity_state = ListField(EmbeddedDocumentField(ActivityState), default=list)
    meta = {
        'collection': 'user_info',
        'indexes': [
            'info.hx_account',
            'activity_state.object_id',
            'activity_state.add_time'
        ]
    }
