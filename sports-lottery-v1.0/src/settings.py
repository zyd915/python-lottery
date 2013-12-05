#coding=UTF-8
__author__ = 'Administrator'
import os
from util.path.path_util import *
from app.vo.ball import *
from app.model.LotteryResult import *

settings_path = os.path.dirname(__file__)
project_root_path = get_parent_path_by_level(settings_path,1)
#sqlite数据库位置
db_file_path = project_root_path + '/resources/database/sqlite-lottery.db'
data_file_dir_path = project_root_path + '/resources/data_files'
# 抽奖记录文件
lottery_file_paths = {
    ball_types['double_color_ball']:data_file_dir_path + '/lottery_double_color.csv',
    ball_types['big_happy_ball']:data_file_dir_path + '/lottery_big_happy.csv',
    ball_types['seven_happy_ball']:data_file_dir_path + '/lottery_seven_happy.csv'
}

# debug状态值
debug_flag = True

# 创建表
def create_table():
    lotteryResult = LotteryResult()
    lotteryResult.db_create_table()

if __name__ == '__main__':
    #print(db_file_path)
    #print(settings_path)
    #print(project_root_path)
    #print(lottery_file_paths[3])

    #创建表
    create_table()