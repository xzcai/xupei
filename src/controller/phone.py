import datetime
import random

from flask import request

from data.database.Mongo.RegisterCode import RegisterCode
from data.database.Sql.User import UserInfo
from src import app
from util.phone_helper import PhoneHelper


# 发送业务处理
def send_bll(phone, code):
    # 查看今天发送的次数
    count = RegisterCode.objects(phone=phone, send_time__gte=datetime.date.today()).count()
    # 查看十分钟内是否发送
    print(datetime.datetime.now() + datetime.timedelta(seconds=-10 * 60))
    register_code = RegisterCode.objects(phone=phone,
                                         send_time__gte=datetime.datetime.now() + datetime.timedelta(
                                                 seconds=-10 * 60)).first()
    # 十分钟内 没有发送
    if register_code is None:
        if count >= 3:
            return '您获取验证码太频繁，请24小时后再试一试'
        else:
            return send_dal(phone, code)
    # 十分钟内有发送
    else:
        if count < 3:
            if register_code.send_count >= 3:
                return '您获取验证码太频繁，请10分钟后再试一试'
            else:
                return send_dal(phone, code, register_code)
        else:
            if register_code.send_count >= 3:
                return '您获取验证码太频繁，请24小时后再试一试'
            else:
                return send_dal(phone, code, register_code)


# 发送验证码（修改数据库或添加新纪录）
def send_dal(phone, code, obj=None):
    if obj is None:
        result = PhoneHelper.send(phone, code)
        if result:
            RegisterCode(phone=phone, send_code=code).save()
            return '发送成功'
        else:
            return '发送失败'
    else:
        result = PhoneHelper.send(phone, code)
        if result:
            obj.send_count += 1
            obj.save()
            return '发送成功'
        else:
            return '发送失败'


def verify_bll(phone, code, type):
    # 取最近发送的验证码
    register_code = RegisterCode.objects(phone=phone, send_code=code, send_type=type).order_by("-send_time").first()
    if register_code is None:
        return '您的验证码不正确，请重新获取'
    else:
        if register_code.send_time + datetime.timedelta(seconds=10 * 60) > datetime.datetime.now():
            return '验证成功'
        else:
            return '您的验证码已经过期，请重新获取'


@app.route("/phone/send")
def send_code():
    phone = request.args.get("phone")
    type = request.args.get('type')

    code = random.randint(100000, 999999)

    if type == "1":  # 注册
        user = UserInfo.query.filter_by(Account=phone).first()
        if user is not None:
            return '该手机号已经被注册'
        else:
            return send_bll(phone, code)
    else:
        return '还未处理'


@app.route("/phone/verify")
def verify():
    phone = request.args.get("phone")
    code = request.args.get("code")
    type = request.args.get('type')

    return verify_bll(phone, code, type)
