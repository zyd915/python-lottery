__author__ = 'Administrator'

#球类型
ball_types = {
    #双色球
    'double_color_ball':1,
    #大乐透
    'big_happy_ball':2,
    #七乐彩
    'seven_happy_ball':3
}
#球色
#红球
color_red = 1
#篮球
color_blue = 2

ball_color_types = {
    'red':color_red,
    'blue':color_blue
}

#红球最小抽取个数
red_ball_count_min = {
    ball_types['double_color_ball']:6,
    ball_types['big_happy_ball']:5,
    ball_types['seven_happy_ball']:7
}
# 红球加注最大值
red_ball_count_max = {
    ball_types['double_color_ball']:20,
    ball_types['big_happy_ball']:35,
    ball_types['seven_happy_ball']:24
}
# 篮球最小抽取个数
blue_ball_count_min = {
    ball_types['double_color_ball']:1,
    ball_types['big_happy_ball']:2,
    ball_types['seven_happy_ball']:0
}
# 篮球加注最大值
blue_ball_count_max = {
    ball_types['double_color_ball']:16,
    ball_types['big_happy_ball']:12,
    ball_types['seven_happy_ball']:0
}

#概率总和基数
rateTotalBase = 1000

# 读取抽奖结果CSV的列头
# 双色球风
columns_of_double_color = ['term', 'red1', 'red2', 'red3', 'red4', 'red5', 'red6','blue1']
# 大乐透
columns_of_big_happy = ['term', 'red1', 'red2', 'red3', 'red4', 'red5', 'blue1','blue2']
# 七乐彩
columns_of_seven_happy = ['term', 'red1', 'red2', 'red3', 'red4', 'red5', 'red6','red7','blue1']

# 根据球类型的到列头
columns_of_type = {
    ball_types['double_color_ball']:columns_of_double_color,
    ball_types['big_happy_ball']:columns_of_big_happy,
    ball_types['seven_happy_ball']:columns_of_seven_happy
}