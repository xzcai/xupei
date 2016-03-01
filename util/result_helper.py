from flask import jsonify


# 成功返回的结果
def result_success(msg, data=[]):
    back_result = {"status": True, 'msg': msg, 'data': data}
    print(back_result)
    return jsonify(back_result)


def result_success_old(msg, data=[]):
    back_result = {"Status": True, 'Msg': msg, 'Data': data}
    print(back_result)
    return jsonify(back_result)


# 失败返回的结果
def result_fail(msg, data=[]):
    back_result = {'status': False, 'msg': msg, 'data': data}
    print(back_result)
    return jsonify(back_result)


def result_fail_old(msg, data=[]):
    back_result = {'Status': False, 'Msg': msg, 'Data': data}
    print(back_result)
    return jsonify(back_result)


# 返回的结果
def result(msg, status=False, data=[]):
    back_result = {'status': status, 'msg': msg, 'data': data}
    print(back_result)
    return jsonify(back_result)
