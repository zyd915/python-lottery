#coding=UTF-8

__author__ = 'zhangyude'


#===========双色球model模型===========#
class Ball(object):

    def __init__(self, color=None, code=None, rate=None):

        #球色
        self.color = color

        #球号
        self.code = code

        #概率
        self.rate = rate

        #概率区段开始
        self.rateStart = 0

        #概率区段结束
        self.rateEnd = 0

        #有效
        self.enable = True

    def __eq__(self, other):
        if other is None or not isinstance(other, Ball):
            return False
        return self.code == other.code

    #失效
    def disable(self):
        self.enable = False

    #释放概率
    def releaseRate(self, ballCount):
        return self.rate/(ballCount*1.0)

    #接收概率
    def receiveRate(self, rate):
        self.rate += rate

    #计算概率区段
    def renderRateRange(self, rateStart):
        self.rateStart = rateStart
        self.rateEnd = self.rate + rateStart