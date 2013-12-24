#coding=UTF-8

__author__ = 'zhangyude'

from util.db.model.fields import *
from util.db.model.models import Model

#球概率
class LotteryRate(Model):

    def __init__(self,ball_type=None, color_type=None, code=None, rate=None, terms=0):

        #球类型
        self.ball_type = IntegerField(name='ball_type', comment=u'球类型', data=ball_type)

        #球颜色
        self.color_type = IntegerField(name='color_type', comment=u'球颜色', data=color_type)

        #球号
        self.code = IntegerField(name='code', comment=u'球号', blank=False, data=code)

        #概率
        self.rate = FloatField(name='rate', comment=u'概率', blank=False, data=rate)

        #期数
        self.terms = IntegerField(name='terms', comment=u'期数', data=terms)