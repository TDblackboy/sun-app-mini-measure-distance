# -*- coding: utf-8 -*-
# @Time : 2022/1/7 13:02
# @Author : 曹沫


class GlobalVar:
    rootPath = './images/'
    suffix = '.jpg'
    prefix = 'p'


def get_rootPath():
    return GlobalVar.rootPath


def get_suffix():
    return GlobalVar.suffix


def get_prefix():
    return GlobalVar.prefix
