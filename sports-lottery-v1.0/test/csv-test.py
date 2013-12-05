#coding=UTF-8
__author__ = 'Administrator'

from csv import *
import unittest

DOUBLE_COLOR_BALL = ['term', 'red1', 'red2', 'red3', 'red4', 'red5', 'red6','blue1']

def readerRow():
    csv_file = reader(open('c:/lottery.csv'))
    for (term, b1,b2,b3,b4,b5,b6,l1) in csv_file:
        print(term+','+b1+'_'+b2+'_'+b3+'_'+b4+'_'+b5+'_'+b6+','+l1)

def readerDic():
    csvFile = open('c:/lottery.csv')
    csvFile.seek(1)
    csvReader = DictReader(csvFile , fieldnames=DOUBLE_COLOR_BALL, restkey='other', restval='111')
    for row in csvReader:
        if row is None or len(row) == 0 or '' in row.values():
            continue
        print(row)
if __name__ ==  '__main__':
    #readerRow()
    readerDic()