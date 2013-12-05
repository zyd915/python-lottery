#coding=UTF-8

__author__ = 'zhangyude'


class ValidateError(Exception):

    def __init__(self, msg):
        self.message = msg

    def getMsg(self):
        return self.message

class SqlError(Exception):
    def __init__(self, msg):
        self.message = msg

    def getMsg(self):
        return self.message

class CsvError(Exception):
    def __init__(self, msg):
        self.message = msg

    def getMsg(self):
        return self.message