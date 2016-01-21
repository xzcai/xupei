from flask import request
from flask.ext.mongoengine import unicode

from data.database.Mongo.MongoUser import MongoUser, Info
from data.database.Sql.User import UserInfo
from data.database.database import mysql
from src import app
from util.Encrypt import BcryptPassManager
from util.hx import HxHelper
from util.image_helper import ImageHelper, PicType
from util.result_helper import result_success, result_fail
import util.token_helper


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

                info = Info(account=user.Account,password=user.Password, pic=user.UserPic, nickname=user.NickName, sex=user.Sex,
                            province=user.Province,
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
    user = MongoUser.objects(info__account=account).first()  # .only('info')  .exclude('info.device_id').all_fields()
    if user is not None and BcryptPassManager.check_valid(password, user.info.password):
        if user.info.is_verify and user.info.device_id != device_id:
            return result_fail('您开启过设备保护，该设备不是常用设备')
        else:
            return util.token_helper.make_token(user.mysql_id, user.info)
    else:
        return result_fail('账号或密码错误')


@app.route("/user/password", methods=['put'])
def modify_password():
    token = request.form.get('token')
    origin_pass = request.form.get("origin_pass")
    new_pass = request.form.get("new_pass")
    return 'ok'


@app.route("/user/test", methods=['get', 'post'])
def user_test():
    pwd = BcryptPassManager.encrypt_pass('123')
    return 'ok'
