__author__ = 'Administrator'
import app.model.LotteryRate as rate
import app.model.LotteryResult as result


def get_rate_list_by_ballType_and_colorType_and_terms(ball_type=None, color_type=None, terms=0):
    if ball_type is None or color_type is None:
        return None
    lotteryRate = rate.LotteryRate(ball_type=ball_type, color_type=color_type, terms=terms)
    rate_list = lotteryRate.fetch_list_by_obj_attributes(conn=lotteryRate.get_conn(), obj=lotteryRate)
    return rate_list

