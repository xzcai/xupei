from data.database.Sql.User import UserInfo
from data.database.database import mysql
from util.result_helper import result_fail, result_success


def modify_password(uid, new_password):
    try:
        UserInfo.query.filter_by(ID=uid).update({UserInfo.Password: new_password})
        mysql.session.commit()
        # MongoUser.objects(mysql_id=uid).update(info__password=new_password)
        return result_success('修改密码成功')
    except Exception as e:
        print('修改密码出错', e)
        return result_fail('修改密码出错' + str(e))
