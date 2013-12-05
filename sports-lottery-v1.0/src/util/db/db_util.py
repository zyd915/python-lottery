#coding=UTF-8

__author__ = 'zhangyude'

import sqlite3
from datetime import *
from util.exceptions import *
from settings import *


exec_success = 1
exec_error = 2


class column_types:
    cInt = "integer"
    cLong = "integer"
    cFloat = "real"
    cStr = "text"
    cBuffer = "blob"

def callBack(call):
    if call is not None and callable(call):
        call()

# 打开数据库
def db_conn(db_file_path):
    try:
        conn = sqlite3.connect(db_file_path)
        return conn
    except Exception as e:
        if debug_flag:
            print(u'连接数据库出现异常：\n'+e.args[0])
        return None

# 执行sql脚本（多条语句）
def execute_sql_script(conn=None, sql_script=None):
    if conn is None or sql_script is None or len(sql_script) == 0:
        return exec_error
    if debug_flag:
        print(sql_script)
    try:
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()
        return exec_success
    except sqlite3.Error as e:
        if debug_flag:
            print(u"执行SQL出现异常：\n" + e.args[0])
        return exec_error

# 执行sql
def execute_sql(conn=None, sql=None, params=None):
    if conn is None or sql is None or len(sql) == 0:
        return exec_error
    if debug_flag :
        print(sql)
    try:
        cursor = conn.cursor()
        if params is not None and len(params) > 0 and type(params[0]) is tuple:
            cursor.executemany(sql, params)
        elif params is not None:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        conn.commit()
        return exec_success
    except sqlite3.Error as e:
        if debug_flag:
            print(u"执行SQL出现异常：\n" + e.args[0])
        return exec_error

# 查询
def query_sql(conn=None, sql=None, params=None):
    if conn is None or sql is None or len(sql) == 0:
        return exec_error
    if debug_flag :
        print(sql)
    try:
        cursor = conn.cursor()
        if params is not None:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor
    except sqlite3.Error as e:
        if debug_flag:
            print(u'执行查询SQL出现异常：\n' + e.args[0])
            raise SqlError(u'查询出现异常')
        return None

# 创建表
def create_table(conn=None, tableName=None, columnItems=None):
    if conn is None or tableName is None or columnItems is None or len(columnItems) == 0:
        return exec_error
    columns = ""
    for item in columnItems:
        columns += item[0] + " " + item[1] + ","
    columns = columns[0:len(columns) - 1]
    sql = u"create table " + tableName + u" ( " + columns + " ) "
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        return exec_success
    except sqlite3.Error as e:
        print(e.args[0])
        return exec_error

# 插入单条数据
def insert_data_one(conn=None, tableName=None, dataItems=None, callFun=None):
    if dataItems is None or len(dataItems) == 0 or tableName is None or conn is None:
        return exec_error
    columnList = []
    dataList = []
    for item in dataItems:
        if type(item) == list:
            columnList.append(item[0])
            dataList.append(item[1])
        else:
            dataList.append(item)
    try:
        sql = None
        if len(columnList) == 0:
            sql = u" insert into " + tableName + u" values ( " + u",".join(iter(dataList)) + u" )"
        else:
            sql = u" insert into " + tableName + u" ( " + u",".join(iter(columnList)) + u" ) values ( " + u",".join(
                iter(dataList)) + u" )"
        execute_state = execute_sql(conn, sql, None)
        conn.commit()
        return execute_state
    except sqlite3.Error as e:
        if debug_flag:
            print(e.args[0])
        return exec_error
    else:
        pass
    finally:
        callBack(callFun)

# 批量插入
def insert_data_many(conn, tableName, columns, dataItems, callFun=None):
    if dataItems is None or len(dataItems) == 0 or tableName is None or conn is None:
        return exec_error
    values = u",".join(u"?" * len(dataItems[0]))
    try:
        sql = None
        if len(columns) == 0:
            sql = u" insert into " + tableName + u" values ( " + values + u" )"
        else:
            sql = u" insert into " + tableName + u" ( " + u",".join(iter(columns)) + u" ) values ( " + values + u" )"
        execute_sql(conn, sql, dataItems)
        conn.commit()
        return exec_success
    except sqlite3.Error as e:
        print(e.args[0])
        return exec_error
    else:
        pass
    finally:
        callBack(callFun)

def delete_by_conditions(conn=None, tableName=None, conditions=None, callFun=None):
    if tableName is None or conn is None or conditions is None:
        return exec_error
    sql = u'delete from ' + tableName + u' where ' + conditions
    try:
        return execute_sql(conn, sql, None)
    finally:
        callBack(callFun)


def update_by_conditions(conn, tableName, dataItems, conditions, callFun=None):
    if dataItems is None or len(dataItems) == 0 or tableName is None or conn is None:
        return exec_error
    updateColumns = ''
    for item in dataItems:
        value = dataItems.get(item)
        if type(value) in (str, datetime, date):
            updateColumns += item + "='" + value + "',"
        else:
            updateColumns += item + "=" + value + ","
    updateColumns = updateColumns.rstrip(',')
    sql = u'update ' + tableName + ' set ' + updateColumns
    if conditions is not None:
        sql += ' where ' + conditions
    try:
        return execute_sql(conn, sql, None)
    finally:
        callBack(callFun)

# 转为数据库条件语句
def to_db_condition(name=None, value=None):
    if name is None or value is None:
        return None
    condition = str(name)
    if isinstance(value, (str, datetime, date)):
        value = "'" + value + "'"
    condition += value
    return condition


class SqlHelper:
    opt_types = {
        'insert':'insert into %(table)( %(columns) ) values ( %(values) ) where %(conditions) ',
        'delete':'delete from %(table) where %(conditions) ',
        'update':'update %(table) set %(values) where %(conditions) ',
        'select':'select %(columns) from %(table) where %(conditions) '
    }

    def __init__(self):
        self.table = None
        self.opt_type = None
        self.sql_header = None
        self.conditions = []
        self.sub_condition = None

    def init_params(self, table=None, opt_type=None, sql_header=None, conditions=None, sub_condition=None):
        self.table = table
        self.opt_type = opt_type
        self.sql_header = sql_header
        self.conditions = conditions
        self.sub_condition = sub_condition

    def addConditionItem(self, key=None, value=None, condition_item=None):
        condition = None
        if condition_item is not None and isinstance(condition_item, str) and len(condition_item) > 0:
            condition = condition_item
        elif key is not None:
            if value is None:
                condition = key + ' is null '
            else:
                condition = to_db_condition(name=key, value=value)
        if condition is not None:
            self.conditions.append(condition)

    def get_sql_conditions(self):
        conditions = ""
        if len(self.conditions) > 0:
            for condition in self.conditions:
                conditions += condition + " and "
        conditions = conditions.rstrip(' and ')
        return conditions

    def get_sql(self):

        return ""

def main():
    conn = db_conn('test.db')
    sql = u"create table test ( code integer, rate integer) "
    insert_sql = u"insert into test(code) values(?)"
    execute_sql(conn=conn, sql=sql)


if __name__ == '__main__':
    main()