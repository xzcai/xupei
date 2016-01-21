from flask import jsonify


# 成功返回的结果
def result_success(msg, data=[]):
    result = {"status": True, "msg": '', 'data': data}
    result['msg'] = msg
    result['data'] = data
    return jsonify(result)


# 失败返回的结果
def result_fail(msg, data=[]):
    result = {'status': False, 'msg': '', 'data': data}
    result['msg'] = msg
    result['data'] = data
    return jsonify(result)




