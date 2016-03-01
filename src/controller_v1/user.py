# 02通过密码登陆
from data.database.Mongo.MongoUser import MongoUser, Token
from data.database.Sql.User import UserInfo
from src import app
from util.Encrypt import BcryptPassManager
from util.decorator_helper import filter_exception
from util.request_helper import request_all_values
from util.result_helper import result_fail, result_success, result_success_old, result_fail_old


@app.route("/API/User/Login", methods=['get', 'post'])
@filter_exception
def user_login_pass_old():
    account, password, device_id = request_all_values('loginName', 'loginPwd', 'mac')
    user = UserInfo.query.filter_by(Account=account).first()

    if user is not None and BcryptPassManager.check_valid(password, user.Password):
        mongo_user = MongoUser.objects(mysql_id=user.ID).first()
        if mongo_user is None:
            return result_fail('数据有误，请联系客服')
        if mongo_user.info.is_verify and mongo_user.info.device_id != device_id:
            return result_fail('您开启过设备保护，该设备不是常用设备')
        else:
            return make_token_old(user.ID)
    else:
        return result_fail('账号或密码错误')


# （在登陆，注册，修改密码时）创建token 并保存token
def make_token_old(user_id):
    try:
        # 创建token
        token_value = BcryptPassManager.encrypt_pass(str(user_id))
        # 查找用户信息
        user = MongoUser.objects(mysql_id=user_id).first()
        # 保存token
        token = Token(value=token_value)
        MongoUser.objects(mysql_id=user_id).update(token=token)
        userInfo = {
            'UID': user.mysql_id,
            'Account': '',
            'Sex': '',
            'Province': user.info.province,
            'City': user.info.city,
            'NickName': user.info.nickname,
            'UserPic': user.info.pic,
            'XPAccount': '',
            'HXAccount': user.info.hx_account,
            'HXPassword': user.info.hx_password,
            'Mood': '',
            'IsVerify': 0,
            'IsProtect': 0
        }
        return result_success_old('成功', {'token': token_value, 'userInfo': userInfo})
    except Exception as e:
        print('创建保存token时出错', e)
        return result_fail_old('失败，创建token时出现异常')
