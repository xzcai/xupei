from src import  mysql

class UserInfo(mysql.Model):
    __tablename__ = 'XP_UserInfo'

    ID = mysql.Column(mysql.Integer, primary_key=True)
    XPAccount = mysql.Column(mysql.String(25), unique=True)
    NickName = mysql.Column(mysql.String(20), unique=True)