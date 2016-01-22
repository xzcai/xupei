import datetime
import random
from flask import request
from data.database.Mongo.PhoneDynamicCode import PhoneDynamicCode
from data.database.Sql.User import UserInfo
from src import app
from util.phone_helper import PhoneHelper
from util.result_helper import result_success, result_fail


# 发送业务处理
def send_bll(phone, code):
    # 查看今天发送的次数
    count = PhoneDynamicCode.objects(phone=phone, send_time__gte=datetime.date.today()).count()
    # 查看十分钟内是否发送
    print(datetime.datetime.now() + datetime.timedelta(seconds=-10 * 60))
    register_code = PhoneDynamicCode.objects(phone=phone,
                                             send_time__gte=datetime.datetime.now() + datetime.timedelta(
                                                     seconds=-10 * 60)).first()
    # 十分钟内 没有发送
    if register_code is None:
        if count >= 3:
            return result_fail('您获取验证码太频繁，请24小时后再试一试')
        else:
            return send_dal(phone, code)
    # 十分钟内有发送
    else:
        if count < 3:
            if register_code.send_count >= 3:
                return result_fail('您获取验证码太频繁，请10分钟后再试一试')
            else:
                return send_dal(phone, code, register_code)
        else:
            if register_code.send_count >= 3:
                return result_fail('您获取验证码太频繁，请24小时后再试一试')
            else:
                return send_dal(phone, code, register_code)


# 发送验证码（修改数据库或添加新纪录）
def send_dal(phone, code, obj=None):
    if obj is None:
        result = PhoneHelper.send(phone, code)
        if result:
            PhoneDynamicCode(phone=phone, send_code=code).save()
            return result_success('发送成功')
        else:
            return result_fail('发送失败')
    else:
        result = PhoneHelper.send(phone, code)
        if result:
            obj.send_count += 1
            obj.save()
            return result_success('发送成功')
        else:
            return result_fail('发送失败')


# 验证验证码 业务处理
def verify_bll(phone, code, type):
    # 取最近发送的验证码
    register_code = PhoneDynamicCode.objects(phone=phone, send_code=code, send_type=type).order_by("-send_time").first()
    if register_code is None:
        return result_fail('您的验证码不正确，请重新获取')
    else:
        if register_code.send_time + datetime.timedelta(seconds=10 * 60) > datetime.datetime.now():
            return result_success('验证成功')
        else:
            return result_fail('您的验证码已经过期，请重新获取')


@app.route("/phone/send")
def send_code():
    phone = request.args.get("phone")
    type = request.args.get('type')

    code = random.randint(100000, 999999)

    try:
        if type == "1":  # 注册
            user = UserInfo.query.filter_by(Account=phone).first()
            if user is not None:
                return result_fail('该手机号已经被注册')
            else:
                return send_bll(phone, code)
        else:
            return '还未处理'
    except Exception as e:
        print('异常错误', e)
        return result_fail('异常错误' + str(e))


@app.route("/phone/verify")
def verify():
    phone = request.args.get("phone")
    code = request.args.get("code")
    type = request.args.get('type')

    try:
        return verify_bll(phone, code, type)
    except Exception as e:
        print('异常错误', e)
        return result_fail('异常错误', + str(e))
