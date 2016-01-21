from data.database.database import mysql


class UserInfo(mysql.Model):
    __tablename__ = 'XP_UserInfo'

    ID = mysql.Column(mysql.Integer, primary_key=True)
    XPAccount = mysql.Column(mysql.String(25), unique=True)
    Account = mysql.Column(mysql.String(25), unique=True)
    Password = mysql.Column(mysql.String(100))
    NickName = mysql.Column(mysql.String(20))
    UserPic = mysql.Column(mysql.String(80))
    Mood = mysql.Column(mysql.String(100),default='')
    Sex = mysql.Column(mysql.Boolean, default=False)
    Phone = mysql.Column(mysql.String(11),default='')
    Email = mysql.Column(mysql.String(20),default='')
    Province = mysql.Column(mysql.String(10),default='')
    City = mysql.Column(mysql.String(20),default='')
    UserOrigin = mysql.Column(mysql.Integer, default=1)
    ThirdID=mysql.Column(mysql.String(20),default='')
    Mac = mysql.Column(mysql.String(35),default='')
    HX_Account = mysql.Column(mysql.String(20),unique=True)
    HX_Password = mysql.Column(mysql.String(32))
    IsVerify = mysql.Column(mysql.BOOLEAN, default=0)
    Is_Protect = mysql.Column(mysql.Integer, default=0)
