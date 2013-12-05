#coding=UTF-8

__author__ = 'zhangyude'
import inspect

# 反射获取类的方法列表
def getMethods(classType):
    methodList = []
    for method in dir(classType):
        if callable(getattr(classType, method)):
            methodList.append(method)
    return methodList

def getFields(classType):
    fieldList = []

    pass