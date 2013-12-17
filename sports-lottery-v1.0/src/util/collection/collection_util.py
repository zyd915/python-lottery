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
    max_list = list1
    min_list = list2
    if len(list1) < len(list2):
        max_list = list2
        min_list = list1
    return [item for item in max_list if item not in min_list]

# 集合并集
def union_section(list1=None, list2=None):
    if list1 is None or list2 is None:
        return
    max_list = list1
    min_list = list2
    if len(list1) < len(list2):
        max_list = list2
        min_list = list1
    differ = [item for item in max_list if item not in min_list]
    return min_list.extend(differ)
