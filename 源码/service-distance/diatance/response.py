# -*- coding: utf-8 -*-
# @Time : 2022/1/5 18:57
# @Author : 曹沫

"""
响应类
    定义静态属性-直接用

"""
from img_util import loadImgBytes


def success(imgPath):
    """
    返回响应内容
    :return:
    """
    return loadImgBytes(imgPath)


def successHeaders():
    return [("Content-Type", "image/jpeg")]


def error():
    return '{"code":"400"}'.encode('utf-8')


def errorHeaders():
    return [("Content-Type", "application/json")]


class HttpResponse:
    status_code200 = '200 OK'
    status_code400 = '400 Error'
