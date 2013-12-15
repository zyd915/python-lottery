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

# 集合交集
def inter_section(list1=None, list2=None):
    if list1 is None or list2 is None:
        return
    return [item for item in list1 if item in list2]

# 集合差集
def differ_section(list1=None, list2=None):
    if list1 is None or list2 is None:
        return
    return [item for item in list1 if item not in list2]
