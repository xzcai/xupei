from flask import request
from data.database.Mongo.MongoUser import MongoUser, Info
from data.database.Sql.User import UserInfo
from data.database.database import mysql
from src import app
from src.bll.user_bll import modify_password
from util.Encrypt import BcryptPassManager
from util.decorator_helper import filter_exception
from util.hx import HxHelper
from util.image_helper import ImageHelper, PicType
from util.result_helper import result_success, result_fail
from util.token_helper import filter_token, make_token


@app.route("/user/register", methods=['get', 'post'])
def user_register():
    account = request.args.get('account')
    password = request.args.get('password')
    pic = request.args.get('pic')

    pic_path = ImageHelper.base64_to_image(pic, PicType.user)
    if pic_path is None:
        return result_fail('上传图片错误')

    nickname = request.args.get('nickname')
    sex = request.args.get('sex')
    province = request.args.get('province')
    city = request.args.get('city')

    try:
        pwd = BcryptPassManager.encrypt_pass(password)
        userinfo = UserInfo.query.filter_by(Account=account).first()
        if userinfo is not None:
            return '该账号已经被注册'
        else:
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


@app.route("/user/login", methods=['get', 'post'])
def user_login():
    account = request.args.get("account")
    password = request.args.get("password")
    device_id = request.args.get("device_id")
    user = UserInfo.query.filter_by(Account=account).first()
    # user111 = MongoUser.objects(mysql_id=220).only('info').first()   .only('info')  .exclude('info.device_id').all_fields()
    # print(user111.info.pic)

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


@app.route("/user/password", methods=['get'])
@filter_exception
@filter_token
def modify(token):
    origin_pass = request.args.get("origin_pass")
    new_pass = request.args.get("new_pass")

    uid = token['id']
    user = UserInfo.query.filter_by(ID=uid).first()
    # user = MongoUser.objects(mysql_id=uid).first()
    if BcryptPassManager.check_valid(origin_pass, user.Password):
        return modify_password(uid, user.Password, BcryptPassManager.encrypt_pass(new_pass))
    else:
        return result_fail('密码输入错误')


@app.route("/user/password_code", methods=['get'])
@filter_exception
@filter_token
def modify_sad(token):
    a = 10 / 0
    print(token)
    return 'pk'


# 设置账户保护
@app.route('/user/protect', methods=['get'])
def set_protect():
    pass


# 设置用户信息
@app.route('/user/info', methods=['get'])
def set_info():
    pass


# 发布用户活动
@app.route('/user/activity', methods=['get'])
def issue_activity():
    pass


@app.route('/user/dynamic', methods=['get'])
def issue_dynamic():
    pass


@app.route("/user/test", methods=['get', 'post'])
def user_test():
    pwd = BcryptPassManager.encrypt_pass('123')
    return 'ok'
