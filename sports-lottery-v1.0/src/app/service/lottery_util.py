#coding=UTF-8
from app.vo import ball, rate
from util.collection import collection_util

__author__ = 'zhangyude'

import random
import copy

# 复制数组
#根据球号获取对应的概率
def _getRateByCode(code, rateList):
    for item in rateList :
        if item.code == code:
            return item.rate
    return 0

# 根据code获取Index
def _getIndexByCode(code, ballList):
    for i in range(len(ballList)):
        if ballList[i].code == code:
            return i
    return -1

#初始化红球列表
def initRedBallList(rateList):
    ballList = []
    for i in range(len(rateList)):
        rate = _getRateByCode(i+1, rateList)
        ballList.append(ball.Ball(ball.color_red, i+1, rate))

    return ballList

#初始化篮球球列表
def initBlueBallList(rateList):
    ballList = []
    for i in range(len(rateList)):
        rate = _getRateByCode(i+1, rateList)
        ballList.append(ball.Ball(ball.color_blue, i+1, rate))

    return ballList

#充值概率区段
def _resetRateRangeList(ballList):
    # 加锁
    # thread.allocate_lock()
    rateRangeInfo = {}
    #概率总和
    rateTotal = 0
    #临时对象
    tempBallList = []
    tempRateBallList = []
    tempBall = None
    #求概率总和
    for item in ballList:
        rateTotal += item.rate
        tempBallList.append(item)

    #求每个球的概率区段
    for item in ballList:
        ballSize = len(tempBallList)
        rangeIndex = random.randint(0, ballSize-1)
        #基数概率区段起始位置
        tempRateStart = 0
        if tempBall != None :
            tempRateStart = tempBall.rateEnd
        #根据随机下标取出的一个球
        tempBall = copy.copy(tempBallList[rangeIndex])
        tempBallList.remove(tempBallList[rangeIndex])
        tempBall.renderRateRange(tempRateStart)
        tempRateBallList.append(tempBall)

    #重置概率区段
    for item in tempRateBallList:
        item.rateStart = round(item.rateStart/(rateTotal*1.0), 4)* rate.rateTotalBase
        item.rateEnd = round(item.rateEnd/(rateTotal*1.0), 4)* rate.rateTotalBase

    #重置球列表
    ballList = tempRateBallList
    # 解锁
    # thread.allocate()
    return ballList

#抽一个红球
def _lotteryOneBall(ballList):
    # 从列表中随机抽取一个
    # 1、先重置概率区段
    ballList = _resetRateRangeList(ballList)
    # 2、取一个随机值
    rateValue = random.randrange(1, rate.rateTotalBase)
    ball = None
    for item in ballList:
        # 根据概率区段获取所对应的球
        if rateValue > item.rateStart and rateValue <= item.rateEnd:
            ball = item
            break
    if ball != None:
        ball.disable()
        # 释放概率
        releaseRate = ball.releaseRate(len(ballList) - 1)
        # 剩下的球增加概率
        for item in ballList:
            if item.enable == True:
                # 接收概率
                item.receiveRate(releaseRate)

    return ball

#抽取一组球
def lotteryBallList(ballCount, ballList):
    lotteryBalls = []
    tempBallList = collection_util.copyList(ballList)
    for i in range(ballCount):
        # 抽出一个球
        ball = _lotteryOneBall(tempBallList)
        lotteryBalls.append(ball)
        # 移除一个
        index = _getIndexByCode(ball.code, tempBallList)
        del tempBallList[index]

    return lotteryBalls

# 抽红球
def lotteryRedBallList(addCount=0, ballList=None, ball_type=ball.ball_types['double_color_ball']):
    if addCount > ball.red_ball_count_max[ball_type] :
        addCount = ball.red_ball_count_max[ball_type]
    elif addCount < ball.red_ball_count_min[ball_type]:
        addCount = ball.red_ball_count_min[ball_type]
    return lotteryBallList(addCount, ballList)

# 抽蓝球
def lotteryBlueBallList(addCount=0, ballList=None, ball_type=ball.ball_types['double_color_ball']):
    if addCount > ball.blue_ball_count_max[ball_type] :
        addCount = ball.blue_ball_count_max[ball_type]
    elif addCount < ball.blue_ball_count_min[ball_type]:
        addCount = ball.blue_ball_count_min[ball_type]
    return lotteryBallList(addCount, ballList)

