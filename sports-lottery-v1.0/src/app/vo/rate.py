#coding=UTF-8

__author__ = 'zhangyude'

#概率总和基数
rateTotalBase = 1000

#球概率
class Rate(object):

    def __init__(self,code=None, rate=None):

        #球号
        self.code = code

        #概率
        self.rate = rate
