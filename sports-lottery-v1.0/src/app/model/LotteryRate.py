#coding=UTF-8

__author__ = 'zhangyude'

from util.db.model.models import *

#概率总和基数
rateTotalBase = 1000

#球概率
class LotteryRate(Model):

    def __init__(self,type=ball_types['double_color_ball'], code=None, rate=None, terms=0):

        #类型
        self.type = IntegerField(name='type', comment=u'类型', data=code)

        #球号
        self.code = IntegerField(name='code', comment=u'球号', blank=False, data=code)

        #概率
        self.rate = FloatField(name='rate', comment=u'概率', blank=False, data=rate)

        #期数
        self.terms = IntegerField(name='terms', comment=u'期数', data=terms)