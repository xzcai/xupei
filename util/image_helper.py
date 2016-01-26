import base64
import uuid

from PIL import Image

from util.result_helper import result_fail


class PicType(object):
    # 用户头像 发布动态 发布活动的图片
    user = 'user'
    # 活动相关的图片
    activity = 'activity'
    # 队列图片
    queue = 'queue'
    # 发现组队图片
    find = 'find'
    # 群头像图片
    qun = 'qun'
    # 银行图片
    bank = 'bank'
    # 标签图片
    label = 'label'


class ImageHelper(object):
    __width = 120
    __height = 120
    # base64 转为图片存储
    @staticmethod
    def base64_to_image(str_base64, pic_type, pic_name=None):
        if pic_name is None:
            pic_name = uuid.uuid1()

        try:
            img_data = base64.b64decode(str_base64)
        except Exception as e:
            print(e, 'base64图片转换出错')
            return None

        try:
            img = open('./imgs/' + pic_type + '/' + str(pic_name) + '.jpg', 'wb')
            img.write(img_data)
            return '/imgs/' + pic_type + '/' + str(pic_name) + '.jpg'
        except Exception as e:
            print(e, '图片存储保存出错')
            return None
        finally:
            img.close()

    # 生成九宫格图片
    @staticmethod
    def sudoku_pic(pics):
        merge_img = Image.new('RGB', (ImageHelper.__width, ImageHelper.__height), 0x808080)
        for img in pics:
            img_small = Image.open(img)
            img_small.thumbnail((30, 30))
            merge_img.paste(img_small, (0, 0))
        merge_img.save('C:/Users/Administrator/Desktop/1111111111111111.jpg', quality=70)
