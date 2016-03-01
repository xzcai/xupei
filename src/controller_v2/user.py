# -*- coding:gbk -*-
import flask
from bson import ObjectId
from flask import request
from data.database.Mongo.MongoUser import MongoUser, Info, ActivityState
from data.database.Sql.User import UserInfo
from data.database.database import mysql
from src import app
from src.bll.user_bll import modify_password
from src.controller_v2.phone import verify_bll
from util.Encrypt import BcryptPassManager
from util.decorator_helper import filter_exception
from util.hx import HxHelper
from util.image_helper import ImageHelper, PicType
from util.request_helper import request_bool, request_xp_account, request_all_values
from util.result_helper import result_success, result_fail, result
from util.token_helper import filter_token, make_token


# 01用户注册
@app.route("/user/register", methods=['get', 'post'])
def user_register():
    account, password, pic, nickname, sex, province, city = request_all_values('account', 'password', 'pic', 'nickname',
                                                                               'sex', 'province', 'city')

    userinfo = UserInfo.query.filter_by(Account=account).first()
    if userinfo is not None:
        return result_fail('该账号已经被注册')

    pic_path = ImageHelper.base64_to_image(pic, PicType.user)
    if pic_path is None:
        # return result_fail('上传图片错误')
        pic_path = '/static/imgs/user/10.jpg'
    if sex == '1':
        sex = True
    else:
        sex = False

    pwd = BcryptPassManager.encrypt_pass(password)

    try:
        if HxHelper.create_account(account, pwd, nickname):
            user = UserInfo(Account=account, Password=pwd, UserPic=pic_path, NickName=nickname, Sex=sex,
                            Province=province, City=city, HX_Account=account, HX_Password=pwd)
            mysql.session.add(user)
            mysql.session.commit()

            info = Info(pic=user.UserPic, nickname=user.NickName, sex=user.Sex, province=user.Province,
                        city=user.City, hx_account=user.HX_Account, hx_password=user.HX_Password)
            mongo_user = MongoUser(mysql_id=user.ID, info=info, token={})
            mongo_user.save()

            return result_success('注册成功')
        else:
            return result_fail('集成环信失败')
    except Exception as e:
        try:
            HxHelper.delete_account(account)
            mysql.session.delete(user)
            mysql.session.commit()
        except Exception as e:
            print(str(e))
            return result_fail(str(e))
        print(str(e))
        return result_fail(str(e))


# 02通过密码登陆
@app.route("/user/login/pass", methods=['get', 'post'])
@filter_exception
def user_login_pass():
    account, password, device_id = request_all_values('account', 'password', 'device_id')
    user = UserInfo.query.filter_by(Account=account).first()

    if user is not None and BcryptPassManager.check_valid(password, user.Password):
        mongo_user = MongoUser.objects(mysql_id=user.ID).first()
        if mongo_user is None:
            return result_fail('数据有误，请联系客服')
        if mongo_user.info.is_verify and mongo_user.info.device_id != device_id:
            return result_fail('您开启过设备保护，该设备不是常用设备')
        else:
            return make_token(user.ID)
    else:
        return result_fail('账号或密码错误')


# 03通过验证码登陆
@app.route("/user/login_code", methods=['get'])
@filter_exception
def user_login_code():
    phone = request.args.get("phone")
    code = request.args.get("code")
    status, msg = verify_bll(phone, code, 2)
    if status is False:
        return result(msg, status)
    user = UserInfo.query.filter_by(Account=phone).first()
    return make_token(user.ID)


# 04修改注册账号
@app.route("/user/account", methods=['get'])
@filter_exception
@filter_token
def modify_account(token):
    uid = token['id']
    phone = request.args.get('phone')
    code = request.args.get('code')
    status, msg = verify_bll(phone, code, 6)
    if status is False:
        return result(msg, status)
    obj = UserInfo.query.filter_by(ID=uid).update({UserInfo.Account: phone})
    mysql.session.commit()
    return make_token(uid)


# 05通过原始密码修改密码
@app.route("/user/password_pass", methods=['get'])
@filter_exception
@filter_token
def modify_pass_by_pass(token):
    origin_pass = request.args.get("origin_pass")
    new_pass = request.args.get("new_pass")

    uid = token['id']
    user = UserInfo.query.filter_by(ID=uid).first()
    # user = MongoUser.objects(mysql_id=uid).first()
    if BcryptPassManager.check_valid(origin_pass, user.Password):
        return modify_password(uid, BcryptPassManager.encrypt_pass(new_pass))
    else:
        return result_fail('密码输入错误')


# 06通过验证码修改密码
@app.route("/user/password_code", methods=['get'])
@filter_exception
@filter_token
def modify_pass_by_code(token):
    new_pass = request.args.get("new_pass")
    uid = token['id']
    return modify_password(uid, BcryptPassManager.encrypt_pass(new_pass))


# 07设置账户保护
@app.route('/user/protect', methods=['get'])
@filter_exception
@filter_token
def set_protect(token):
    uid = token['id']
    type = request.args.get("type")
    device_id = request.args.get("device_id")
    if type == "1":
        type = True
    else:
        type = False
    MongoUser.objects(mysql_id=uid).update_one(info__device_id=device_id, info__is_protect=type)
    return result_success("设置成功")


# 08设置用户信息
@app.route('/user/info', methods=['get'])
@filter_exception
@filter_token
def set_info(token):
    uid = token['id']

    # 修改昵称
    nickname = request.args.get('nickname')
    if nickname is not None:
        MongoUser.objects(mysql_id=uid).update_one(info__nickname=nickname)

    # 修改头像
    pic = request.args.get('pic')
    if pic is not None:
        MongoUser.objects(mysql_id=uid).update_one(info__pic=pic)

    # 修改个性签名
    signature = request.args.get('signature')
    if signature is not None:
        MongoUser.objects(mysql_id=uid).update_one(info__signature=signature)

    # 修改性别
    sex = request_bool('sex', False)
    if isinstance(sex, bool):
        MongoUser.objects(mysql_id=uid).update_one(info__sex=sex)
    else:
        return sex

    # 修改省市
    province = request.args.get('province')
    city = request.args.get('city')
    if province is not None and city is not None:
        MongoUser.objects(mysql_id=uid).update_one(info__province=province, info__city=city)

    return result_success('修改成功')


# 09设置许陪号
@app.route('/user/xp_account', methods=['get'])
@filter_exception
@filter_token
def set_xp_account(token):
    uid = token['id']
    xp_account = request_xp_account('xp_account')
    if isinstance(xp_account, flask.wrappers.Response):
        return xp_account

    user = MongoUser.objects(mysql_id=uid).only('info').first()
    if user.info.xp_account is None:
        MongoUser.objects(mysql_id=uid).update_one(info__xp_account=xp_account)
        return result_success('许陪号设置成功')
    else:
        return result_fail('许陪号只能设置一次，不能在重新设置')


# 10发布用户活动
@app.route('/user/activity', methods=['get', 'post'])
@filter_exception
@filter_token
def issue_activity(token):
    is_friend, is_city, content, address, begin_time, pics = request_all_values('is_friend', 'is_city', 'content',
                                                                                'address', 'begin_time', 'pics')
    pic_array = []
    if pics is not None:
        for pic in pics.split('|'):
            pic_path = ImageHelper.base64_to_image(pic, PicType.activity)
            if pic_path is None:
                return result_fail('上传图片错误')
            pic_array.append(pic_path)
    if is_friend == 'true':
        is_friend = True
    if is_city == 'true':
        is_city = True

    activity_state = ActivityState(active_type=3, object_id=ObjectId(), content=content, pics=pic_array,
                                   address=address, begin_time=begin_time, is_friend=is_friend, is_city=is_city)
    MongoUser.objects(mysql_id=token['id']).update_one(add_to_set__activity_state=activity_state)
    return result_success('发布活动成功')


# 11发布用户动态
@app.route('/user/dynamic', methods=['get', 'post'])
@filter_exception
@filter_token
def issue_dynamic(token):
    is_friend, is_city, content, address, log, lat, pics = request_all_values('is_friend', 'is_city', 'content',
                                                                              'address', 'log', 'lat', 'pics')
    if is_friend == 'true':
        is_friend = True
    if is_city == 'true':
        is_city = True

    pic_array = []
    if pics is not None:
        for pic in pics.split('|'):
            pic_path = ImageHelper.base64_to_image(pic, PicType.activity)
            if pic_path is None:
                return result_fail('上传图片错误')
            pic_array.append(pic_path)

    activity_state = ActivityState(active_type=4, object_id=ObjectId(), content=content, pics=pic_array,
                                   address=address,
                                   longitude=log, latitude=lat, is_friend=is_friend, is_city=is_city)
    MongoUser.objects(mysql_id=token['id']).update_one(add_to_set__activity_state=activity_state)
    return result_success('发布动态成功')
