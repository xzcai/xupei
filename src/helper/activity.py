# 活动帮助类，一些格式转换之类的额
import time


# 活动时间格式转换
def time_transform(begin_time, end_time):
    begin_str = begin_time.strftime("%Y-%m-%d")
    end_str = end_time.strftime("%Y-%m-%d")

    begin_array = time.strptime(begin_str, "%Y-%m-%d")
    begin_month = str(begin_array.tm_mon)
    begin_day = str(begin_array.tm_mday)

    if begin_str == end_str:
        return begin_month + '月' + begin_day + '日'
    else:
        end_array = time.strptime(end_str, "%Y-%m-%d")
        end_month = str(end_array.tm_mon)
        end_day = str(end_array.tm_mday)
        return begin_month + '月' + begin_day + '日-' + end_month + '月' + end_day + '日'
