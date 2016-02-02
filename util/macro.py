code_send_mean = ((1, '注册'),
                  (2, '登陆'),
                  (3, '安全验证'),
                  (4, '买票'),
                  (5, '修改密码'),
                  (6, '修改手机号'),
                  (7, '添加银行卡'),
                  (8, '删除银行卡'),
                  (9, '提现'),
                  (10, '退票'))

active_state_type = ((1, '推荐'),
                     (2, '参加'),
                     (3, '发布'),
                     (4, '动态'),
                     (5, '姿态'))

# 加解密 密钥
ENCRYPT_KEY = 'benhu_xupei'

cast_status = (
    (1, '免费'),
    (2, '自费'),
    (3, '既有免费')
)


class Activity_Attribute(object):
    new = '1'
    hot = "2"
    recommend = "3"
    free = "4"
    near = "5"
    select = "6"
