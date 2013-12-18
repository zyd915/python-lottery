__author__ = 'Administrator'
import app.model.LotteryRate as lottery_rate
import app.model.LotteryResult as lottery_result
import app.config as config

def get_rate_list_by_ballType_and_colorType_and_terms(ball_type=None, color_type=None, terms=0):
    if ball_type is None or color_type is None:
        return None
    lotteryRate = lottery_rate.LotteryRate(ball_type=ball_type, color_type=color_type, terms=terms)
    rate_list = lotteryRate.fetch_list_by_obj_attributes(conn=lotteryRate.get_conn(), obj=lotteryRate)
    return rate_list


def init_lottery_result_to_db(ball_type=None, result_csv_file_path=None):
    if ball_type not in config.ball_types.values() or result_csv_file_path is None:
        return
    result_list = lottery_result.load_from_csv(type=ball_type, csv_file_path=result_csv_file_path)
    if result_list is not None:
        for result in result_list:
            lotteryResult = lottery_result.LotteryResult(type=ball_type, term=result[lottery_result.key_term],
                                                         redBalls=result[lottery_result.key_red_balls], blueBalls=result[lottery_result.key_blue_balls])
            lotteryResult.save(conditions="term <> '" + result[lottery_result.key_term] +"'")

