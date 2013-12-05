#coding=UTF-8
__author__ = 'Administrator'

import csv
import io
from util.exceptions import *

def parseItemByRow(iteratorObj=None, parseItemFun=None, conditionsFun=None):
    if iteratorObj is None:
        return
    rows = csv.reader(iteratorObj)
    itemList = []
    for columns in rows:
        if parseItemFun is not None and callable(parseItemFun):
            if conditionsFun is not None and callable(conditionsFun):
                if conditionsFun(columns):
                    item = parseItemFun(fields=columns)
                    if item is not None:
                        itemList.append(item)
            else:
                item = parseItemFun(fields=columns)
                itemList.append(item)
    if len(itemList) > 0:
        return itemList


def parseItemByDictRow(iteratorObj=None, hasHeader=False, fieldNames=None, parseItemFun=None, conditionsFun=None):
    if iteratorObj is None:
        return
    if fieldNames is None and isinstance(iteratorObj, io.IOBase):
        if hasHeader :
            iteratorObj.seek(0)
        else:
            raise CsvError(u'parseItemByDictRow, you should set hasHeader=True or set fieldNames ')
    rows = csv.DictReader(iteratorObj, fieldnames=fieldNames)
    itemList = []
    for columns in rows:
        if parseItemFun is not None and callable(parseItemFun):
            if conditionsFun is not None and callable(conditionsFun):
                if conditionsFun(columns):
                    item = parseItemFun(fields=columns)
                    if item is not None:
                        itemList.append(item)
            else:
                item = parseItemFun(fields=columns)
                if item is not None:
                    itemList.append(item)
    if len(itemList) > 0:
        return itemList



# For Test
def parseItemFun(**kwargs):
    type = kwargs['type']
    print(type)
    fields = kwargs['fields']
    if fields is None or len(fields) == 0:
        return None
    columns = ['term', 'red1', 'red2', 'red3', 'red4', 'red5', 'red6','blue1']
    term = fields[columns[0]]
    #red_balls = [fields[ball] for ball in fields if ball not in (columns[0], columns[7])]
    red_balls = [fields[ball] for ball in fields if ball in (columns[1:-1])]
    blue_balls = fields[columns[7]]
    item = (term,red_balls,blue_balls)
    print(item)
    return item


# For Test
def conditions(fields):
    return fields is not None and fields[0] == '13111'


if __name__ == '__main__':
    columns = ['term', 'red1', 'red2', 'red3', 'red4', 'red5', 'red6','blue1']

    #parseItemByRow(iteratorObj=open('c:/lottery1.csv'), parseItemFun=(lambda fs: parseItemFun(fs)), conditionsFun=(lambda fs:conditions(fs)))
    list = parseItemByDictRow(iteratorObj=open('c:/lottery.csv'), hasHeader=False, fieldNames=columns, parseItemFun=lambda fields=None:parseItemFun(type=2,fields=fields))
    #print(list)