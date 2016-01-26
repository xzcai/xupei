import datetime
import random
from flask import request
from data.database.Mongo.PhoneDynamicCode import PhoneDynamicCode
from data.database.Sql.User import UserInfo
from src import app
from util.decorator_helper import filter_exception
from util.phone_helper import PhoneHelper
from util.result_helper import result_success, result_fail, result


# 发送业务处理
def send_bll(phone, code, type):
    # 查看今天发送的次数
    count = PhoneDynamicCode.objects(phone=phone, send_time__gte=datetime.date.today(), send_type=type).count()
    # 查看十分钟内是否发送
    register_code = PhoneDynamicCode.objects(phone=phone, send_time__gte=datetime.datetime.now() + datetime.timedelta(
            seconds=-10 * 60), send_type=type).first()
    # 十分钟内 没有发送
    if register_code is None:
        if count >= 3:
            return result_fail('您获取验证码太频繁，请24小时后再试一试')
        else:
            return send_dal(phone, code, type)
    # 十分钟内有发送
    else:
        if count < 3:
            if register_code.send_count >= 3:
                return result_fail('您获取验证码太频繁，请10分钟后再试一试')
            else:
                return send_dal(phone, code, type, register_code)
        else:
            if register_code.send_count >= 3:
                return result_fail('您获取验证码太频繁，请24小时后再试一试')
            else:
                return send_dal(phone, code, type, register_code)


# 发送验证码（修改数据库或添加新纪录）
def send_dal(phone, code, type, obj=None):
    if obj is None:
        result = PhoneHelper.send(phone, code)
        if result:
            PhoneDynamicCode(phone=phone, send_code=code, send_type=type).save()
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
    code_obj = PhoneDynamicCode.objects(phone=phone, send_code=code, send_type=type).order_by("-send_time").first()
    if code_obj is None:
        return False, '您的验证码不正确，请重新获取'
    else:
        if code_obj.send_time + datetime.timedelta(seconds=10 * 60) > datetime.datetime.now():
            return True, '验证成功'
        else:
            return False, '您的验证码已经过期，请重新获取'


# 发送验证码
@app.route("/phone/send")
@filter_exception
def send_code():
    phone = request.args.get("phone")
    type = request.args.get('type')
    code = random.randint(100000, 999999)
    #  type=1:注册； type=2:登陆；type=3:安全验证(账号保护)；type=4:买票；type=5:修改密码；type=6 修改手机号;type=7 添加银行卡；type=8 删除银行卡；type=9 提现;type=10 退票；11 主办方绑定手机号
    if type == "1" or type == "6":  # 注册
        user = UserInfo.query.filter_by(Account=phone).first()
        if user is not None:
            return result_fail('该手机号已经被注册')
        else:
            return send_bll(phone, code, int(type))
    elif type == "2" or type == "5":
        user = UserInfo.query.filter_by(Account=phone).first()
        if user is not None:
            return send_bll(phone, code, int(type))
        else:
            return result_fail('该手机号尚未注册')
    else:
        return '还未处理'


# 验证验证码
@app.route("/phone/verify")
@filter_exception
def verify():
    phone = request.args.get("phone")
    code = request.args.get("code")
    type = request.args.get('type')

    status, msg = verify_bll(phone, code, type)
    return result(msg, status)
