#coding=UTF-8

__author__ = 'zhangyude'

#Ball_type
ball_types = {
    #双色球
    'double_color_ball':1,
    #大乐透
    'big_happy_ball':2,
    #七乐彩
    'seven_happy_ball':3
}
#Color_Enum
#红球
color_red = 1
#篮球
color_blue = 2

#红球的号码区间
code_red_range = range(1, 33, 1)
#篮球的号码区间
code_blue_range = range(1, 16, 1)

#红球个数
red_ball_count_min = 6
# 红球加注最大值
red_ball_count_max = 20
# 篮球个数
blue_ball_count_min = 1
# 篮球加注
blue_ball_count_max = 16

#===========双色球model模型===========#
class Ball(object):

    def __init__(self, color, code, rate):

        #类型
        self.type = type

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