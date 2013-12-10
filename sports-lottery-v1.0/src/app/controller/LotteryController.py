#coding=UTF-8

__author__ = 'zhangyude'

# test
from app.service import lottery_util
from app.vo.rate import Rate
from app.vo.ball import Ball
import app.config as config

class LotteryController(object):

    def __init__(self):
       object.__init__(self)

    # 根据球类型加载球列表: (list[红球]， list[篮球])
    def load_ball_list(self, ball_type=None):

        """
        @param ball_type: 球类型【双色球，大乐透，双色球】
        """
        pass

    # 抽奖（支持胆拖式）
    def lottery(self, ball_type=config.ball_types['double_color_ball'], ball_count=None,
                positive_red_balls=None, positive_red_balls_count=None,
                positive_blue_balls=None, positive_blue_balls_count=None):
        """
        @param ball_type: 球类型
        @param ball_count: 球个数
        @param positive_red_balls: 认为红球可能出现的号码
        @param positive_red_balls_count: 认为红球可能出现的号码的个数
        @param positive_blue_balls: 认为篮球可能出现的号码
        @param positive_blue_balls_count: 认为篮球可能出现的号码的个数
        """
        red_ball_count = config.red_ball_count_min[ball_type]

        pass

    def _validator_ball_code(self, select_code_list=None, ball_list=None):
        """
        验证待选球号码是否在供选球号码列表里面
        @param select_code_list: 待选球号码列表
        @param ball_list: 供选球列表
        @return:
        """
        if select_code_list is None or len(select_code_list) == 0 or ball_list is None or len(ball_list) == 0:
            return False
        for select_code in select_code_list:
            has = False
            for ball in ball_list :
                if isinstance(ball, Ball) and ball.code == select_code:
                    has = True
                    break
            if not has:
                return False
        return True

    def _validator_ball_count(self, ball_type=None, color_type=None, count=0, isMax=False):
        """
        验证球个数是否超过供选个数范围
        @param ball_type:
        @param color_type:
        @param count:
        @param isMax:
        @return:
        """
        if ball_type not in config.ball_types.values() or color_type not in config.ball_color_types.values():
            return False

        if color_type == config.color_red:
            if isMax:
                if count > config.red_ball_count_max[ball_type]:
                    return False
            else:
                if count < config.red_ball_count_min[ball_type]:
                    return False
        elif color_type == config.color_blue:
            if isMax:
                if count > config.blue_ball_count_max[ball_type]:
                    return False
            else:
                if count < config.blue_ball_count_min[ball_type]:
                    return False

        return True
    # 导入抽奖结果到数据库中
    @staticmethod
    def init_lottery_result_to_db(ball_type=None):

        pass

    # 初始化抽奖概率到数据库中
    @staticmethod
    def init_lottery_rate_to_db(terms=None):

        pass


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