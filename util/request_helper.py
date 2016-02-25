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
        return result_fail(args_name + ' 参数格式错误')


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


# 对必须输入的参数进行验证
def request_required(*args_name):
    for name in args_name:
        if request.args.get(name) is None:
            return result_fail(name + ' 参数是必须的')


# (输入所有参数名)获取所有的参数值
def request_all_values(*args_name):
    values = []
    if request.method == 'GET':
        for name in args_name:
            values.append(request.args.get(name))
    else:
        for name in args_name:
            values.append(request.form.get(name))
    return values

# 返回int 类型必填参数
# def test_2(label):
#     def _test_1(func):
#         def __test_1():
#             d = request.args.get(label)
#             if d is None:
#                 return result_fail(label + " 是必须的")
#             return func()
#
#         return __test_1
#
#     return _test_1
# def request_required_int(*args)
#     def _request_required_int(func):
#         def __request_required_int():
#             args_value = request.args.get(args_name)
#             if args_value is None:
#                 return result_fail(args_name + ' 参数是必须的')
#             else:
#                 return int(args_value)
#             return func()
#         return __request_required_int
#     return _request_required_int
