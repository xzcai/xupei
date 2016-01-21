from util.token_helper import make_token
from flask import request


# （注册 登陆 修改密码） 成功后修改token和返回的用户信息
def user_success(user):
    # 修改返回token
    token = make_token(user)
    if token is None:
        return False, None
    else:
        data = {'token': token, "userinfo": user}
        return True, data


# 判断token是否过期
def handle_token():
    if request.method == 'POST':
        token=request.form.get('token')
    else:
        token=request.form.get('token')


