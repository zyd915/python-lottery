__author__ = 'Administrator'

from util.db.db_util import *
import settings
if __name__ == '__main__':
    sql = u'select * from LotteryResult'
    cursor = query_sql(conn=db_conn(settings.db_file_path), sql=sql)
    rows = cursor.fetchall()
    for row in rows:
        print(row)