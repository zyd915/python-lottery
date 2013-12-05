#coding=UTF-8

__author__ = 'zhangyude'

# test
from app.service import lottery_util
from app.vo.rate import Rate

class Lottery(object):
    # 红色球基数
    redBallCount = 6
    # 蓝色球基数
    blueBallCount = 1
    # 红球概率列表
    redRateList = [33, 33, 33, 33, 33, 33, 33, 33, 33, 33,
                   33, 33, 33, 33, 33, 33, 33, 33, 33, 33,
                   33, 33, 33, 33, 33, 33, 33, 33, 33, 33,
                   33, 33, 33]
    # 篮球概率列表
    blueRateList = [16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
                    16, 16, 16, 16, 16, 16, ]

    def __init__(self):
       object.__init__(self)



def main():
    redBallRateList = []
    blueBallRateList = []

    redBallRateList.append(Rate(1, 19))
    redBallRateList.append(Rate(2, 22))
    redBallRateList.append(Rate(3, 18))
    redBallRateList.append(Rate(4, 22))
    redBallRateList.append(Rate(5, 17))
    redBallRateList.append(Rate(6, 19))
    redBallRateList.append(Rate(7, 20))
    redBallRateList.append(Rate(8, 16))
    redBallRateList.append(Rate(9, 17))
    redBallRateList.append(Rate(10, 14))
    redBallRateList.append(Rate(11, 16))
    redBallRateList.append(Rate(12, 19))
    redBallRateList.append(Rate(13, 23))
    redBallRateList.append(Rate(14, 20))
    redBallRateList.append(Rate(15, 20))
    redBallRateList.append(Rate(16, 12))
    redBallRateList.append(Rate(17, 24))
    redBallRateList.append(Rate(18, 18))
    redBallRateList.append(Rate(19, 21))
    redBallRateList.append(Rate(20, 17))
    redBallRateList.append(Rate(21, 16))
    redBallRateList.append(Rate(22, 20))
    redBallRateList.append(Rate(23, 22))
    redBallRateList.append(Rate(24, 15))
    redBallRateList.append(Rate(25, 17))
    redBallRateList.append(Rate(26, 19))
    redBallRateList.append(Rate(27, 18))
    redBallRateList.append(Rate(28, 19))
    redBallRateList.append(Rate(29, 15))
    redBallRateList.append(Rate(30, 15))
    redBallRateList.append(Rate(31, 18))
    redBallRateList.append(Rate(32, 18))
    redBallRateList.append(Rate(33, 14))

    blueBallRateList.append(Rate(1, 2))
    blueBallRateList.append(Rate(2, 5))
    blueBallRateList.append(Rate(3, 8))
    blueBallRateList.append(Rate(4, 1))
    blueBallRateList.append(Rate(5, 5))
    blueBallRateList.append(Rate(6, 11))
    blueBallRateList.append(Rate(7, 9))
    blueBallRateList.append(Rate(8, 5))
    blueBallRateList.append(Rate(9, 8))
    blueBallRateList.append(Rate(10, 4))
    blueBallRateList.append(Rate(11, 8))
    blueBallRateList.append(Rate(12, 6))
    blueBallRateList.append(Rate(13, 7))
    blueBallRateList.append(Rate(14, 10))
    blueBallRateList.append(Rate(15, 3))
    blueBallRateList.append(Rate(16, 8))

    initRedBalls = lottery_util.initRedBallList(redBallRateList)
    initBlueBalls = lottery_util.initBlueBallList(blueBallRateList)

    for i in range(35):
        lotteryRedBalls = lottery_util.lotteryRedBallList(6, initRedBalls)
        lotteryBlueBalls = lottery_util.lotteryBlueBallList(1, initBlueBalls)

        redBalls = []
        blueBalls = []

        s1 = u"==========第"
        s2 = u"次抽奖============"
        num = i+1
        print(s1+ str(num) + s2)
        print(u"红色球号码是：")
        for item in lotteryRedBalls:
            redBalls.append(item.code)
        redBalls.sort()
        print(redBalls)
        print(u"蓝色球号码是：")
        for item in lotteryBlueBalls:
            blueBalls.append(item.code)
        blueBalls.sort()
        print(blueBalls)


if __name__ == '__main__':
    main()