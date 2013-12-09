#coding=UTF-8

__author__ = 'zhangyude'

from app.model.LotteryResult import LotteryResult

# 创建表
def create_table():
    lotteryResult = LotteryResult()
    lotteryResult.db_create_table()

if __name__ == '__main__':

    #创建表
    create_table()