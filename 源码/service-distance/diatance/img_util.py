# -*- coding: utf-8 -*-
# @Time : 2022/1/5 21:54
# @Author : 曹沫
import time
from io import BytesIO

from PIL import Image


def save(fullPath, content):
    """
    :param fullPath: 保存位置
    :param content: binary 保存的内容
    """

    # 保存为str类型
    # content = str(content)
    # fileObject = open("str_file", "w")
    # fileObject.write(content)
    # fileObject.close()

    # 原始数据保存，不一定是图片
    # fileObject = open("binary_test.jpg", "ab")
    # fileObject.write(content)
    # fileObject.close()

    # 原始数据保存成图片
    image = Image.open(BytesIO(content))
    # print(save_path + imageName)
    image.save(fullPath)
    # print('save origin image to:' + fullPath)


def loadImgBytes(imgPath):
    with open(imgPath, 'rb') as f:
        content = f.read()
        # print(content)
        # print(type(content))
        return content
