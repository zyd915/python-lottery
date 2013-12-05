#coding=UTF-8
__author__ = 'Administrator'

from util.db.model.models import *
from util.csv.csv_reader import *

# 从txt文件中获取抽奖结果集
# 格式：双色球
# 2013139,_07_08_11_13_21_27,_08
# 格式：大乐透
# 13109,_13_20_26_29_32,_02_06
# 七乐彩
# 2013138,_07_09_13_16_17_26_28,_05

columns_of_double_color = ['term', 'red1', 'red2', 'red3', 'red4', 'red5', 'red6','blue1']
columns_of_big_happy = ['term', 'red1', 'red2', 'red3', 'red4', 'red5', 'blue1','blue2']
columns_of_seven_happy = ['term', 'red1', 'red2', 'red3', 'red4', 'red5', 'red6','red7','blue1']

columns_of_type = {
    ball_types['double_color_ball']:columns_of_double_color,
    ball_types['big_happy_ball']:columns_of_big_happy,
    ball_types['seven_happy_ball']:columns_of_seven_happy
}

# 解析结果回调函数
def parseItemFun(**kwargs):
    type = kwargs['type']
    fields = kwargs['fields']
    if type is None or type not in ball_types.values() or fields is None or len(fields) == 0:
        return None
    columns = None
    red_balls = None
    blue_balls = None
    columns = columns_of_type[type]
    term = fields[columns[0]]
    if type == ball_types['double_color_ball']:
        red_balls = [fields[ball] for ball in fields if ball in (columns[1:-1])]
        blue_balls = fields[columns[-1]]
    elif type == ball_types['big_happy_ball']:
        red_balls = [fields[ball] for ball in fields if ball in (columns[1:-2])]
        blue_balls = [fields[ball] for ball in fields if ball in (columns[-2:])]
    elif type == ball_types['seven_happy_ball']:
        red_balls = [fields[ball] for ball in fields if ball in (columns[1:-1])]
        blue_balls = fields[columns[-1]]
    return (term, red_balls, blue_balls)

# 解析结果条件回调函数
def conditionsFun():
    return True

#
def load_from_csv(type=ball_types['double_color_ball'],csv_file_path=None):
    if csv_file_path is None or type not in ball_types.values():
        return None
    columns = columns_of_type[type]
    resultFile = open(csv_file_path)
    list = parseItemByDictRow(
        iteratorObj=resultFile,
        hasHeader=False,
        fieldNames=columns,
        parseItemFun=lambda fields=None: parseItemFun(type=type, fields=fields)
        )
    if list is not None or len(list) > 0:
        return list
    else:
        return None

# 抽奖结果
class LotteryResult(Model):

    def __init__(self, type=None, term=None, redBalls=None, blueBalls=None):

        super(LotteryResult, self).__init__(_tableName='LotteryResult')

        # 期号
        self.term = CharField(name='terms', comment=u'期号',unique=True, blank=False, data=term)

        # 抽奖类型（ball_type）
        self.type = IntegerField(name='type', comment=u'抽奖类型', blank=False, data=type)

        # 红球
        self.redBalls = CharField(name='redBalls', comment=u'红球', blank=False, data=redBalls)

        # 篮球
        self.blueBalls = CharField(name='blueBalls', comment=u'篮球', blank=False, data=blueBalls)

        #def


if __name__ == '__main__':
    list = load_from_csv(type=ball_types['double_color_ball'], csv_file_path='c:/lottery.csv')

    for item in list:
        print(item)

    print(columns_of_type)
