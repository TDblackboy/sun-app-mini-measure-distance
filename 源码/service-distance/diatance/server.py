# -*- coding: utf-8 -*-
# @Time : 2021/12/19 19:40
# @Author : 曹沫
# 功能：启动服务（等待http请求）

from http_filter import HttpFilter
from http_parser import HttpParser
from img_handler import Distance
import response

"""
接受OS接口传来的请求信息并处理

规定:
    通过http传输图片
    图片格式:输入手机照片jpg,输出也是jpg

"""


class DistanceServer:
    def __init__(self):
        print("创建DistanceServer实例")
        self.__filter = HttpFilter()
        self.__parser = HttpParser()
        self.__response = response.HttpResponse()

    def acceptRequest(self, environ, start_response):
        """
        处理过程
        （1）过滤请求-必须是指定类型
        （2）接受图片，（保存到本地？）
        （3）分析图片
        （4）返回分析后的图片:错误的话返回json，正确的话返回image

        # 响应回调设置:状态码、响应头、响应体
        # re = start_response('200 OK', [
        #     ('Content-Type', 'application/json'),
        #     ('Content-Length', str(len(body)))
        # ])
        """
        if self.__filter.filter(environ):
            imageName = self.__parser.parse(environ)

            savePath = Distance().compute(imageName)
            print(savePath)

            # 响应:状态码、响应头、响应体
            start_response(self.__response.status_code200, response.successHeaders())
            return [response.success(savePath)]
        else:
            print("错误的请求")
            start_response(self.__response.status_code400, response.errorHeaders())
            return [response.error()]
