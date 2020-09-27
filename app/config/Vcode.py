# -*- coding: utf-8 -*-
"""
@Date : '2020-06-18'
@Desc :
"""
import os
from io import BytesIO
from random import randint
from PIL import Image, ImageFont, ImageDraw


class vcode:
    def __init__(self, width=100, height=34, size=4):
        self.width = width
        self.height = height
        self.size = size
        self.__code = ''  # 验证码字符串
        self.pen = None  # 画笔

    @property  # 装饰器访问私有化属性
    def code(self):
        return self.__code

    def generate(self):
        # 1.创建画布，颜色随机
        im = Image.new("RGB", (self.width, self.height), self.__rand_color(150))
        self.pen = ImageDraw.Draw(im)  # 在画布上创建画笔
        # 2.生成验证码字符串
        self.__rand_string()
        # 3.画验证码
        self.__draw_code()
        # 4.画干扰点
        self.__draw_point()
        # 5.画干扰线
        self.__rand_line()
        # 6.返回验证码图片
        buf = BytesIO()  # 缓冲区
        im.save(buf, 'png')  # 以pug格式将图片保存在缓冲区
        res = buf.getvalue()  # 获取图片的二进制
        return res

    # 创建个随机颜色的函数，数字越接近0颜色越浓，越接近255颜色越淡
    def __rand_color(self, min=0, max=255):
        return randint(min, max), randint(min, max), randint(min, max)

    # 生成验证码字符串
    def __rand_string(self):
        self.__code = ""  # 每次生成字符串前将之前缓存字符串重置为空
        for i in range(self.size):
            self.__code += str(randint(0, 9))

    # 画验证码
    def __draw_code(self):
        # 加载字体
        grader_father = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        path = os.path.join(grader_father, 'static/fonts/SIMLI.TTF')
        # 设置字体大小和编码格式
        font1 = ImageFont.truetype(font=path, size=25, encoding="utf-8")
        # 计算字符串宽度
        width = (self.width - 20) // self.size
        # 逐个画字
        for i in range(len(self.__code)):
            x = 13 + width * i  # 计算字符的x坐标
            # 写入字，并随机颜色
            self.pen.text((x, 7), self.__code[i], font=font1, fill=self.__rand_color(0, 80))

    # 画点
    def __draw_point(self):
        for i in range(100):
            self.pen.point((randint(1, self.width - 1), randint(1, self.height - 1)), self.__rand_color(30, 100))

    # 画线
    def __rand_line(self):
        for i in range(5):
            # 逐个画线，随机起始点和结束点，并随机颜色
            self.pen.line([(randint(1, self.width - 1), randint(1, self.height - 1)),
                           (randint(1, self.width - 1), randint(1, self.height - 1))], fill=self.__rand_color(50, 150),
                          width=2)


vc = vcode()  # 单例属性
