import base64
import uuid

from PIL import Image


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
    # 用户发布动态图片
    dynamic = 'dynamic'


class ImageHelper(object):
    __border = 120

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
            img = open('./src/static/imgs/' + pic_type + '/' + str(pic_name) + '.jpg', 'wb')
            img.write(img_data)
            return '/static/imgs/' + pic_type + '/' + str(pic_name) + '.jpg'
        except Exception as e:
            print(e, '图片存储保存出错')
            return None
        finally:
            try:
                img.close()
            except Exception as e:
                pass

    # 生成九宫格图片
    @staticmethod
    def sudoku_pic(pics, qid):
        try:
            img_path = '/static/imgs/qun/' + qid + '.jpg'
            merge_img = Image.new('RGB', (ImageHelper.__border, ImageHelper.__border), 0x808080)
            if len(pics) == 1:
                return pics[0]
            else:
                border, position = ImageHelper.position_size(pics, ImageHelper.__border)
                for i in range(0, len(pics)):
                    try:
                        img = Image.open(pics[i])
                        box = ImageHelper.clip_image(img.size)
                        img_small = img.crop(box)
                        img_small.thumbnail((border, border))
                        merge_img.paste(img_small, position[i])
                    except Exception as e:
                        print('生成九宫格出错' + str(e))
                    finally:
                        img.close()
                merge_img.save('.' + img_path)
                return img_path
        except Exception as e:
            print('生成九宫格出错' + str(e))
        finally:
            merge_img.close()

    # 切图
    @staticmethod
    def clip_image(size):
        width = int(size[0])
        height = int(size[1])
        if width > height:
            dx = width - height
            box = (int(dx / 2), 0, int(height + dx / 2), height)
        else:
            dx = height - width
            box = (0, int(dx / 2), width, int(width + dx / 2))
        return box

    # 确定小图大小和位置
    @staticmethod
    def position_size(pics, length=140):
        n = len(pics)
        margin = 2
        if n <= 4:
            border = int((length - margin * 3) / 2)
        else:
            border = int((length - margin * 4) / 3)
        if n == 1:
            return pics[0]
        elif n == 2:
            position = [(margin, int((length - border) / 2)), (border + 4, int((length - border) / 2))]
        elif n == 3:
            position = [(int((length - border) / 2), 2), (2, border + 4), (border + 4, border + 4)]
        elif n == 4:
            position = [(2, 2), (border + 4, 2), (2, border + 4), (border + 4, border + 4)]
        elif n == 5:
            position = [(2 + int(border / 2), (2 + int(border / 2))),
                        ((int(border / 2) + border + 4), (2 + int(border / 2))),
                        (2, (int(border / 2) + border + 4)), (border + 4, (int(border / 2) + border + 4)),
                        (2 * border + 6, (int(border / 2) + border + 4))
                        ]
        elif n == 6:
            position = [(2, int(border / 2) + 2), (border + 4, int(border / 2) + 2),
                        (2 * border + 6, int(border / 2) + 2),
                        (2, (3 * border / 2) + 4), (border + 4, (3 * border / 2) + 4),
                        (2 * border + 6, (3 * border / 2) + 4)]
        elif n == 7:
            position = [(border + 4, 2),
                        (2, 4 + border), (border + 44 + border), (2 * border + 6, 4 + border),
                        (2, 2 * border + 6), (border + 4, 2 * border + 6), (2 * border + 6, 2 * border + 6)]
        elif n == 8:
            position = [(int(border / 2) + 2, 2), (int(3 * border / 2) + 4, 2),
                        (2, 4 + border), (border + 4, 4 + border), (2 * border + 6, 4 + border),
                        (2, 2 * border + 6), (border + 4, 2 * border + 6), (2 * border + 6, 2 * border + 6)]
        else:
            position = [(2, 2), (border + 4, 2), (2 * border + 6, 2),
                        (2, 4 + border), (border + 4, 4 + border), (2 * border + 6, 4 + border),
                        (2, 2 * border + 6), (border + 4, 2 * border + 6), (2 * border + 6, 2 * border + 6)]

        return border, position


