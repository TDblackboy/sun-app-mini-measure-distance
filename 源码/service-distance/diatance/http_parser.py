# -*- coding: utf-8 -*-
# @Time : 2022/1/5 11:02
# @Author : 曹沫

"""
解析HTTP请求的解析器
    单拎出来、后期“更改解析规则”，解耦

核心方法：parser() - 解析http传输报文中的image二进制数据，保存到本地，交给识别程序处理

重点：
    （1）如果：图片上传的方式post，form-data
    解析请求体中的信息
    明确这种上传方式的“数据分割规则”

    （2）直接用binary格式上传

"""
import time

import img_util
import config


class HttpParser:
    def __init__(self):
        self.content_length = 'CONTENT_LENGTH'
        self.input = 'wsgi.input'
        # self.content_type = 'CONTENT_TYPE'

    def parse(self, environ):
        # self.look_env(environ)
        # 接受图片数据:图片的名字-自定义-根据日期、图片本身的数据
        # 解析出原始数据binary-bytes类型
        content_length = int(environ.get(self.content_length, 0))
        # print(content_length)
        request_body = environ[self.input].read(content_length)

        # 保存原始图片
        imageName = time.strftime("%Y-%m-%d-%H%M%S", time.localtime())
        fullPath = config.get_rootPath() + imageName + config.get_suffix()
        img_util.save(fullPath, request_body)
        return fullPath

    @staticmethod
    def look_env(environ):
        # environ带有那些信息：
        print(type(environ))
        for item in environ.items():
            print(item)

    def parseBoundary(self, environ):
        contentType = environ[self.content_type]
        # print(type(contentType))
        # print(contentType)
        boundary = contentType.split(';')[1].split('=')[1]
        # 50 bytes
        # print(len(boundary))
        return boundary

    @staticmethod
    def parseRequestBody(content, boundary=''):
        # content = str(content)
        # print(boundary)

        # 分割
        # splits = content.split(boundary)
        # splits = content.splitlines('\r\n')
        # print(len(splits))
        # print(splits[0])
        # print(splits[1])
        # print(splits[2])

        print(content)
