import re

from flask import request

# 获取参数 返回相应的bool值
from util.result_helper import result_fail


# 输入参数 1(0), true(false)  返回bool值
def request_bool(args_name, required=True):
    if request.method == 'GET':
        args_value = request.args.get(args_name)
    else:
        args_value = request.form.get(args_name)
    if required and args_value is None:
        return result_fail(args_name + ' 参数是必须的')

    if args_value == "1" or args_value.lower() == 'true':
        return True
    elif args_value == "0" or args_value.lower() == 'false':
        return False
    else:
        return result_fail(args_name + ' 参数拼写错误')


# 对许陪号进行验证
def request_xp_account(args_name, required=True):
    if request.method == 'GET':
        args_value = request.args.get(args_name)
    else:
        args_value = request.form.get(args_name)
    if required and args_value is None:
        return result_fail(args_name + ' 参数是必须的')

    regular_expression = '(?!^\d+$)(?!^[a-zA-Z]+$)[0-9a-zA-Z]{6,10}'
    ver_reslt = bool(
            re.match(r"" + str(regular_expression) + "",
                     args_value, re.VERBOSE))
    if ver_reslt:
        return args_value
    else:
        return result_fail(args_name + ' 许陪号只能是【6-10】位的字母和数字组合')
