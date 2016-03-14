import datetime

from mongoengine import Document, IntField, StringField, BooleanField, DateTimeField, ListField, EmbeddedDocumentField, \
    EmbeddedDocument


class Member(EmbeddedDocument):
    name = StringField()
    id = StringField()


class Sponsor(Document):
    mysql_id = IntField(primary_key=True)
    pic = StringField(required=True)
    name = StringField(required=True)
    type = IntField(choices=(1, 2, 3, 4, 5))
    is_pass = BooleanField(default=False)
    add_time = DateTimeField(required=True, default=datetime.datetime.now())
    p_name = StringField(default='') # 组织，企业，团队名称
    p_id = StringField(default='') # 营业执照注册号，组织机构代码
    operator_name = StringField(default='') # 运营者姓名
    operator_id = StringField(default='') # 运营者身份证id
    introduce = StringField(default='')
    hx_group_id = StringField(required=True)
    activity_count = IntField(default=0) # 活动举办次数
    focus_count = IntField(default=0)       # 关注人数
    teams = ListField(EmbeddedDocumentField(Member))
    meta = {
        'collection': 'user_info',
        'indexes': [
            'hx_group_id'
        ]
    }
