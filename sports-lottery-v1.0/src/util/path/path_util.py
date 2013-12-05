#coding=UTF-8
__author__ = 'Administrator'

import os

# 获取指定目录的父目录
def get_parent_path(path=None):
    if path is None or len(path) == 0 or not os.path.exists(path):
        return None

    parent_path = os.path.abspath(os.path.join(path, os.path.pardir))
    if os.path.exists(parent_path):
        return parent_path
    else:
        return None

def get_parent_path_by_level(path=None, level=1):
    parent_path = path
    for i in range(level):
        parent_path = get_parent_path(parent_path)
    return parent_path


if __name__ == '__main__' :

    parent_path = get_parent_path_by_level('C:\Intel\ExtremeGraphics\CUI\Resource',level=3)
    print(parent_path)
