import datetime
import time


# 时间转为时间戳
def time_to_stamp(obj_time):
    date_str = obj_time.strftime("%Y-%m-%d %H:%M:%S")
    time_array = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(time_array))


# 时间戳转为时间
def stamp_to_time(obj_stamp):
    time_array = time.localtime(int(obj_stamp))
    date_str = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')


# 时间添加
def time_add(obj_time, second):
    return obj_time + datetime.timedelta(second=second)
