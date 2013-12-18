#coding=UTF-8

__author__ = 'zhangyude'

# test
from app.service import lottery_util
from app.vo.rate import Rate
from app.vo.ball import Ball
import app.config as config
from util.collection.collection_util import *
from app.service.LotteryService import *

# 多实例运行
class LotteryController(object):

    def __init__(self):
       object.__init__(self)

    # 根据球类型加载球列表
    def load_ball_list(self, ball_type=None, color_type=None, terms=0):
        """
        @param ball_type: 球类型【双色球，大乐透，双色球】
        @param color_type: 球颜色【红球，蓝球】
        """
        rate_list = self.get_rate_list(ball_type=ball_type, color_type=color_type, terms=terms)
        return lottery_util.initBallList(rateList=rate_list, color_type=color_type)

    # 获取概率列表
    def get_rate_list(self, ball_type=None, color_type=None, terms=0):
        if ball_type is None or color_type is None:
            return None
        return get_rate_list_by_ballType_and_colorType_and_terms(ball_type=ball_type, color_type=color_type, terms=terms)


    # 抽奖（支持胆拖式）
    # 1、单注 参数：None
    # 2、复式（多注）参数：球数
    # 3、胆拖（胆码列表 + 拖码个数）参数：胆码球列表 + 拖码球个数
    # 4、定胆杀号（胆码球号列表+杀号列表+拖码个数）
    def lottery(self, ball_type=None, color_type=None, ball_count=0, terms=0,
                positive_ball_list=None, possible_ball_list=None,
                possible_ball_count=0, not_possible_list=None):
        """
        @param ball_type: 球类型
        @param color_type: 球颜色
        @param ball_count: 球个数
        @param positive_ball_list: 胆码列表
        @param possible_ball_list: 拖码列表
        @param possible_ball_count: 拖码个数
        @param not_possible_list: 杀号列表
        """
        if ball_type not in config.ball_types.values() or color_type not in config.ball_color_types.values():
            return None

        ball_list = self.load_ball_list(ball_type=ball_type, color_type=color_type, terms=terms)
        # 验证球个数
        lottery_ball_count = len(positive_ball_list or []) + possible_ball_count
        lottery_ball_count = ball_count or lottery_ball_count
        if not self._validator_ball_count(ball_type=ball_type, color_type=color_type, count=lottery_ball_count):
            return None
        # 验证球号码
        if positive_ball_list is not None and not self._validator_ball_code(select_code_list=positive_ball_list, ball_type=ball_type):
            return None
        if possible_ball_list is not None and not self._validator_ball_code(select_code_list=possible_ball_list, ball_type=ball_type):
            return None
        if not_possible_list is not None and not self._validator_ball_code(select_code_list=not_possible_list, ball_type=ball_type):
            return None

        lottery_code_list = []
        disable_code_list = []
        # 胆码
        lottery_code_list.extend(positive_ball_list or [])
        disable_code_list = [code for code in lottery_code_list]
        # 杀号
        if not_possible_list is not None:
            disable_code_list.extend([code for code in not_possible_list])
        # 拖码
        if lottery_ball_count > len(lottery_code_list) and possible_ball_list is not None and possible_ball_count > 0:
            lottery_code_list.extend([ball.code for ball in lottery_util.lotteryBallList(possible_ball_count, possible_ball_list)])
            disable_code_list.extend([code for code in possible_ball_list])
        elif lottery_ball_count > len(lottery_code_list) and possible_ball_list is None and possible_ball_count > 0:
            filter_to_lottery_ball_list = self._filter(filter_code_list=disable_code_list, ball_list=ball_list)
            lottery_count = lottery_ball_count - len(lottery_code_list)
            lottery_code_list.extend([ball.code for ball in lottery_util.lotteryBallList(lottery_count, filter_to_lottery_ball_list)])

        # 复式机选
        if len(lottery_code_list) == 0 and ball_count > 0:
            lottery_code_list.extend([ball.code for ball in lottery_util.lotteryBallList(ball_count, ball_list)])

        return lottery_code_list

    # 过滤
    def _filter(self, filter_code_list=None, ball_list=None):
        if filter_code_list is None or ball_list is None:
            return
        filter_ball_list = [Ball(code=item.code) for item in filter_code_list]
        return differ_section(filter_ball_list, ball_list)


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

    def _validator_ball_count(self, ball_type=None, color_type=None, count=0):
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
            if count > config.red_ball_count_max[ball_type] or count < config.red_ball_count_min[ball_type]:
                return False
        elif color_type == config.color_blue:
            if count > config.blue_ball_count_max[ball_type] or count < config.blue_ball_count_min[ball_type]:
                return False

        return True

    # 导入抽奖结果到数据库中
    @staticmethod
    def init_lottery_result_to_db(ball_type=None, result_csv_file_path=None):
        init_lottery_result_to_db(ball_type=ball_type, result_csv_file_path=result_csv_file_path)

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

    initRedBalls = lottery_util.initBallList(rateList=redBallRateList, color_type=config.color_red)
    initBlueBalls = lottery_util.initBallList(rateList=blueBallRateList, color_type=config.color_blue)

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