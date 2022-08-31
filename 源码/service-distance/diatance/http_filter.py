# -*- coding: utf-8 -*-
# @Time : 2022/1/5 11:07
# @Author : 曹沫

"""
过滤器
    单拎出来、后期“更改过滤规则”，解耦

核心方法：filter
    过滤请求:post,传输数据为image，
    限制：1、post； 2、自定义字段send:image； 3、ACCEPT字段维image
    :return: true or false
"""


class HttpFilter:
    def __init__(self):
        self.httpMethod = 'POST'
        # 请求的API Path
        # /maybe 项目的名称
        # /md:MeasuringDistance的缩写
        self.httpRequestPath = '/maybe/md'
        self.contentType = 'image/'

        # self.httpSend = 'image'
        # self.httpAcceptType = 'image/'

    def filter(self, environ):
        # print('过滤')
        # environ带有那些信息：
        # print(type(environ))
        # for item in environ.items():
        #     print(item)
        # print(environ['REQUEST_METHOD'])
        # print(environ['HTTP_ACCEPT'])
        # print(environ['PATH_INFO'])
        # print(environ['HTTP_SEND'])
        # print(environ['QUERY_STRING'])

        # 必须是post请求
        if environ['REQUEST_METHOD'] != self.httpMethod:
            return False
        # 传输类型必须是图片:自定义请求头中字段 'send'：'image'
        # if environ['HTTP_SEND'] != self.httpSend:
        #     return False
        # 接受类型必须是image/
        # if self.httpAcceptType not in environ['HTTP_ACCEPT']:
        #     return False
        # 请求路径必须为 /maybe/md
        if environ['PATH_INFO'] != self.httpRequestPath:
            return False
        if self.contentType not in environ['CONTENT_TYPE']:
            return False
        return True
