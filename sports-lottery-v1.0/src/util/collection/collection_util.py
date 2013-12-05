#coding=UTF-8

__author__ = 'zhangyude'

# 集合复制
def copyList(collection):
    if collection == None :
        return []
    tempCollection = []
    for item in collection:
        tempCollection.append(item)
    return tempCollection