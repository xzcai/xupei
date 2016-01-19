from flask import request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy.testing import db

from data.database.Mongo.MongoUser import MongoUser, Info
from data.database.Sql.User import UserInfo
from data.database.database import mysql
from src import app
from util.Encrypt import EncryptPass
from util.hx import HxHelper
from util.macro import result


@app.route("/user/register", methods=['get'])
def user_register():
    account = request.args.get('account')
    password = request.args.get('password')
    pic = request.args.get('pic')
    nickname = request.args.get('nickname')
    sex = request.args.get('sex')
    province = request.args.get('province')
    city = request.args.get('city')

    pwd = EncryptPass(password)
    userinfo = UserInfo(Account=account, Password=pwd, UserPic=pic, NickName=nickname, Sex=sex,
                        Province=province, City=city, HX_Account=account, HX_Password=pwd)

    try:
        user = UserInfo.query.filter_by(Account=account).first()
        if user is not None:
            return '该账号已经被注册'
        else:
            if HxHelper.create_account(account, pwd, nickname):
                mysql.session.add(userinfo)
                mysql.session.commit()

                info = Info(nickname=nickname, pic=pic)
                mongo_user = MongoUser(mysql_id=userinfo.ID, info=info)
                mongo_user.save()

                result['Status'] = True
                result['Msg'] = '注册成功'
                return jsonify(result)
            else:
                result['Status'] = False
                result['Msg'] = '集成环信失败'
                return jsonify(result)
    except Exception as e:
        HxHelper.delete_account(account)
        mysql.session.delete(userinfo)
        mysql.session.commit()

        result['Msg'] = e
        print('11111', 'df')
        print(jsonify(result))
        return jsonify(result)


@app.route("/user/login", methods=['post'])
def user_login():
    return 'dsf'
