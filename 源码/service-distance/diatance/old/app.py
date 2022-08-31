# -*- coding: utf-8 -*-
# @Time : 2021/12/19 19:55
# @Author : 曹沫
#

from urllib.parse import parse_qs


def run(environ, start_response):
    """
    处理过程
        （1）过滤请求-必须是指定类型
        （2）接受图片，（保存到本地？）
        （3）分析图片
        （4）返回分析后的图片:错误的话返回json，正确的话返回image
    """
    if filterRequest(environ):
        print("处理图片")
        # 接受图片数据<---------------------------------??!!!
        long = int(environ.get("CONTENT_LENGTH", 0))
        data = environ["wsgi.input"].read(long).decode('utf-8')
        data = parse_qs(data)
        print(data)

        body = '<h1>nice</h1>'
        re = start_response('200 OK', [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(body)))
        ])
        return [body.encode('utf-8')]
    else:
        print("错误的请求")
        body = '{"code":"400"}'
        re = start_response('400 Error', [('Content-Type', 'application/json')])
        # print(re)
        return [body.encode('utf-8')]


def filterRequest(environ):
    """
    过滤请求:post,传输数据为image，
    :return: true or false
    """
    # print(type(environ))
    # for item in environ.items():
    #     print(item)
    # print(environ[''])

    # 必须是post请求
    if environ['REQUEST_METHOD'] != 'POST':
        print(environ['REQUEST_METHOD'])
        return False
    # 传输类型必须是图片:自定义请求头中字段 'send'：'image'
    if environ['HTTP_SEND'] != 'image':
        print(environ['HTTP_SEND'])
        return False

    # 接受类型必须是image/
    if 'image/' not in environ['HTTP_ACCEPT']:
        print(environ['HTTP_ACCEPT'])
        return False
    # print(environ['PATH_INFO'])
    # print(environ['QUERY_STRING'])
    return True
