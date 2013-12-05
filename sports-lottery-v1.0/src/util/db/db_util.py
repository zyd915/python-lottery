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
def query_sql(conn, sql, params=None):
    if conn is None or sql is None or len(sql) == 0:
        return exec_error
    if debug_flag :
        print(sql)
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor
    except sqlite3.Error as e:
        if debug_flag:
            print(u'执行查询SQL出现异常：\n' + e.args[0])
        raise SqlError(u'查询出现异常')

# 创建表
def create_table(conn, tableName, columnItems):
    if columnItems is None or len(columnItems) == 0:
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
def insert_data_one(conn, tableName, dataItems, callFun=None):
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
        execute_sql(conn, sql, None)
        conn.commit()
        return exec_success
    except sqlite3.Error as e:
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

def delete_by_conditions(conn, tableName, conditions, callFun=None):
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



def main():
    conn = db_conn('test.db')
    sql = u"create table test ( code integer, rate integer) "
    insert_sql = u"insert into test(code) values(?)"
    execute_sql(conn=conn, sql=sql)


if __name__ == '__main__':
    main()