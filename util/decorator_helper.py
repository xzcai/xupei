from functools import wraps

from util.result_helper import result_fail


# 异常过滤
def filter_exception(func):
    @wraps(func)
    def _filter_exception(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print('异常错误', str(e))
            return result_fail('异常错误--->' + str(e))

    return _filter_exception