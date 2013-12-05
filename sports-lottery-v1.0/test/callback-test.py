#coding=UTF-8
__author__ = 'Administrator'

def callBack(close=False):
    if close is True:
        print('callBack')

def doCall(callFun=None):
    if callFun is not None and callable(callFun):
        callFun()

if __name__ == '__main__':
    doCall(callBack)