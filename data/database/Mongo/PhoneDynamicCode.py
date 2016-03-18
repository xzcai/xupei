import datetime

from mongoengine import StringField, IntField, BooleanField
from data.database.database import mongo

#  type=1:注册； type=2:登陆；type=3:安全验证(账号保护)；type=4:买票；type=5:修改密码；type=6 修改手机号;type=7 添加银行卡；type=8 删除银行卡；type=9 提现;type=10 退票；11 主办方绑定手机号
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
