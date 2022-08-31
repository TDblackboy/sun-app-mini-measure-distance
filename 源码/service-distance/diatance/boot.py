# -*- coding: utf-8 -*-
# @Time : 2022/1/5 10:34
# @Author : 曹沫

"""
启动类
    运行服务

# tcp、http连接、解析的动作？！交由其他库/框架处理
#       (1)WSGI：Web Server Gateway Interface。<---
#       (2)FastAPI
# 按Ctrl+C终止服务器。

"""
from wsgiref.simple_server import make_server

from server import DistanceServer
import configparser


class ServerBoot:
    # 默认
    ip = 'localhost'
    port = 8001

    def __init__(self):
        self.server = DistanceServer()
        self.config()

    def run(self):
        print("service:distance measurement starting...")
        # 创建一个服务器，IP地址为空，端口是8001，处理函数是acceptRequest():
        httpd = make_server(ServerBoot.ip, ServerBoot.port, self.server.acceptRequest)

        print('serving HTTP on {0}:{1}...'.format(ServerBoot.ip, ServerBoot.port))
        # 开始监听HTTP请求:
        httpd.serve_forever()

    @staticmethod
    def config():
        """
        读取配置
        :return:
        """
        cf = configparser.ConfigParser()
        cf.read('./setting.conf')
        ServerBoot.ip = cf.get('address', 'ip')
        ServerBoot.port = cf.getint('address', 'port')


if __name__ == '__main__':
    ServerBoot().run()
