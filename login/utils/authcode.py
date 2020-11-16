# coding=utf-8

"""
Author: Yao Zhao
Create Date: 2020-10-14
@Software: Pycharm
"""

import os
import string
import random
from io import BytesIO
from PIL import Image,ImageDraw,ImageFont
from mysite import settings  # 项目中的settings文件，配置了BASEDIR路径，在这里无需关注


def get_authcode_img(request):
    """
    获取随机验证码，带干扰噪点，
    :param request: request请求，用于将验证码存放在session中
    :return: 返回验证码图片的数据内容
    """
    def get_background_color():  # 定义一个获取图片背景/噪点颜色的函数，产生浅色
        color = tuple((random.choices(range(160,256),k=3)))
        return color

    def get_content_color():  # 定义一个获取文字颜色的函数，产生深色
        color = tuple((random.choices(range(0,100),k=3)))
        return color

    img_obj = Image.new("RGB",(117,34),get_background_color())  # 创建一个图片对象
    draw_obj = ImageDraw.Draw(img_obj)  # 通过图片对象生成一个画笔对象
    font_path = os.path.join(settings.BASE_DIR,"statics","font","cerepf__.ttf")  # 获取字体，注意有些字体无法显示数字
    font_obj = ImageFont.truetype(font_path,32)  # 创建一个字体对象
    random_code = ''  # 用户验证的字符串
    all_char = string.ascii_letters+string.digits
    for i in range(4):
        a = random.choice(all_char)
        random_code += a

    draw_obj.text((22,-3),random_code,fill=get_content_color(),font=font_obj)

    width = 117
    height = 34

    # 添加噪线
    for i in range(5):  # 添加5条干扰线
        # 两个坐标点确定一条线
        x1 = random.randint(0,width)
        y1 = random.randint(0,height)
        x2 = random.randint(0,width)
        y2 = random.randint(0,height)
        draw_obj.line((x1,y1,x2,y2),fill=get_background_color())  # 画噪线

    # 添加噪点
    for i in range(30):
        draw_obj.point((random.randint(0,width),random.randint(0,height)),fill=get_background_color())


    f = BytesIO()  # 生成内存操作符-句柄
    img_obj.save(f,"png")  # 将图片存在内存中
    data = f.getvalue()
    # 获取句柄中的内容

    # # 存验证码方式：1.存在全局变量（不可取，多个用户会顶替）2.存在各自客户的session中
    # # 方式1
    # global valid_str
    # valid_str = random_code

    # 方式二，推荐
    request.session["authcode"] = random_code
    return data
