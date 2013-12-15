__author__ = 'Administrator'


from app.model.LotteryResult import *

if __name__ == '__main__':
    list = load_from_csv(type=ball_types['double_color_ball'], csv_file_path='c:/lottery.csv')

    for item in list:
        print(item)

    print(columns_of_type)