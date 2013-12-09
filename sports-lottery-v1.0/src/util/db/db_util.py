#coding=UTF-8

__author__ = 'zhangyude'

import sqlite3
import datetime
import settings


exec_success = 1
exec_error = 2

debug_flag = settings.debug_flag

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
            raise e
        return None

# 执行sql脚本（多条语句）
def execute_sql_script(conn=None, sql_script=None):
    if conn is None or sql_script is None or len(sql_script) == 0:
        return exec_error
    if debug_flag:
        print(u'执行SQL脚本：')
        print(sql_script)
    try:
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()
        return exec_success
    except sqlite3.Error as e:
        if debug_flag:
            print(u"执行SQL出现异常：\n" + e.args[0])
            raise e
        return exec_error

# 执行sql
def execute_sql(conn=None, sql=None, params=None):
    if conn is None or sql is None or len(sql) == 0:
        return exec_error
    if debug_flag :
        print(u'执行SQL：')
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
            raise e
        return exec_error

# 查询
def query_sql(conn=None, sql=None, params=None):
    if conn is None or sql is None or len(sql) == 0:
        return exec_error
    if debug_flag :
        print(u'Query执行SQL：')
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
            raise e
        return None

# 插入单条数据
def insert_one_by_dataDict_conditions(conn=None, tableName=None, dataDict=None, conditions=None, callFun=None):
    if dataDict is None or len(dataDict) == 0 or tableName is None or conn is None:
        return exec_error
    try:
        sql = SqlHelper(table=tableName, opt_type=SqlHelper.opt_types['insert'])
        sql.set_columns_and_values(columns=dataDict.keys(), values=dataDict.values())
        sql.add_conditions(conditions)
        insert_sql = sql.get_sql()
        if debug_flag:
            print(insert_sql)
        execute_state = execute_sql(conn, insert_sql, None)
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

# 插入单条数据
def insert_one_by_columns_values_conditions(conn=None, tableName=None, columns=None, values=None, conditions=None, callFun=None):
    if values is None or len(values) == 0 or tableName is None or conn is None:
        return exec_error
    try:
        sql = SqlHelper(table=tableName, opt_type=SqlHelper.opt_types['insert'])
        sql.set_columns_and_values(columns=columns, values=values)
        sql.add_conditions(conditions)
        insert_sql = sql.get_sql()
        if debug_flag:
            print(insert_sql)
        execute_state = execute_sql(conn, insert_sql, None)
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
def insert_data_many(conn=None, tableName=None, columns=None, dataItems=None, callFun=None):
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


def update_by_conditions(conn=None, tableName=None, dataDict=None, conditions=None, callFun=None):
    if dataDict is None or len(dataDict) == 0 or tableName is None or conn is None:
        return exec_error
    sql = SqlHelper(table=tableName, opt_type=SqlHelper.opt_types['update'], conditions=conditions)
    sql.add_keyValues(dataDict)
    sql_update = sql.get_sql()
    try:
        return execute_sql(conn, sql_update, None)
    finally:
        callBack(callFun)

# 转为数据库条件语句
def to_db_condition(name=None, value=None):
    if name is None or value is None:
        return None
    condition = name
    if type(value) in (str, datetime.datetime, datetime.date):
        value = "'" + value + "'"
    condition +='=' + _to_sql_str(value)
    return condition

def _to_sql_str(value):
    if type(value) != str:
        return str(value)
    else:
        return u"'"+value+u"'"

class SqlHelper:
    opt_types = {
        'insert':'insert',
        'delete':'delete',
        'update':'update',
        'select':'select'
    }
    sql_templates = {
        'insert':u'insert into %(table)s %(columns)s values ( %(values)s ) where %(conditions)s ',
        'delete':u'delete from %(table)s where %(conditions)s ',
        'update':u'update %(table)s set %(keyValues)s where %(conditions)s ',
        'select':u'select %(columns)s from %(table)s where %(conditions)s '
    }
    param_types = {
        'table':'table',
        'columns':'columns',
        'values':'values',
        'keyValues':'keyValues',
        'conditions':'conditions'
    }
    conditions_default = '1=1'

    def __init__(self, table=None, opt_type=None, conditions=None):
        self.table = table
        self.opt_type = opt_type
        self.conditions = conditions or []
        self.columns = []
        self.values = []
        self.keyValues = []
        if opt_type is not None and opt_type in SqlHelper.opt_types:
            self.sql_template = SqlHelper.sql_templates[opt_type]
        else:
            self.sql_template = None
        self.sql_conditions = None
        self.sql_sub_script = None

    def set_sql_sub_script(self, sql_sub_script):
        self.sql_sub_script = sql_sub_script

    def set_sql_conditions(self, sql_conditions):
        self.sql_conditions = sql_conditions


    def set_columns_and_values(self, columns=None, values=None):
        columns = columns or []
        values = values or []
        if type(columns) != list or type(values) != list: return
        self.columns.extend(columns)
        self.values.extend(values)

    def add_column(self, column):
        if column is None or column in self.columns : return
        self.columns.append(column)

    def add_condition(self, key=None, value=None):
        condition = None
        if key is not None:
            if value is None:
                condition = key + ' is null '
            else:
                condition = to_db_condition(name=key, value=value)
        if condition is not None:
            self.conditions.append(condition)

    def add_conditions(self, conditions):
        if conditions is None or type(conditions) != list : return
        self.conditions.extend(conditions)

    def add_keyValue(self, key=None, value=None):
        if key is None : return
        keyValue = key +'='+_to_sql_str(value)
        self.keyValues.append(keyValue)

    def add_keyValues(self, keyValues):
        keyValues = keyValues or []
        if len(keyValues) == 0: return
        kvList = []
        if type(keyValues) == dict and len(keyValues) > 0:
            for key in keyValues:
                kv = key + "=" + _to_sql_str(keyValues[key])
                kvList.append(kv)
        elif type(keyValues) == list:
            kvList = keyValues
        else:
            return
        self.keyValues.extend(kvList)

    def get_sql_columns(self):
        columns = u''
        if len(self.columns) > 0:
            columns = u','.join(iter(self.columns))
        return columns

    def get_sql_values(self):
        values = u''
        if len(self.values) > 0:
            values = u','.join(iter([_to_sql_str(value) for value in self.values]))
        return values

    def get_sql_keyValues(self):
        keyValues = u''
        if len(self.keyValues) > 0:
            keyValues = u','.join(iter(self.keyValues))
        return keyValues

    def get_sql_conditions(self):
        if self.sql_conditions is not None and len(self.sql_conditions) > 0:
            return self.sql_conditions
        conditions = u''
        if len(self.conditions) > 0:
            conditions = u" and ".join(iter(self.conditions))
        else:
            conditions = SqlHelper.conditions_default
        return conditions

    def get_sql(self):
        if self.sql_template is None: return None
        template = self.sql_template
        columns = self.get_sql_columns()
        values = self.get_sql_values()
        keyValues = self.get_sql_keyValues()
        conditions = self.get_sql_conditions()
        if self.opt_type == self.opt_types['insert'] and columns != u'':
                columns = u'('+ columns + u')'
        params = {
            self.param_types['table']:self.table,
            self.param_types['columns']:columns,
            self.param_types['values']:values,
            self.param_types['keyValues']:keyValues,
            self.param_types['conditions']:conditions
        }
        template = template % params
        sql = template
        if self.sql_sub_script is not None:
            sql = template + self.sql_sub_script
        if self.opt_type == self.opt_types['update'] and (self.keyValues is None or len(self.keyValues) == 0):
            return None
        if debug_flag:
            print(sql)
        return sql



def main():
    conn = db_conn('test.db')
    sql = u"create table test ( code integer, rate integer) "
    insert_sql = u"insert into test(code) values(?)"
    execute_sql(conn=conn, sql=sql)


if __name__ == '__main__':
    ##main()
    #l = None
    #s = l or []
    #print(s)

    # test insert
    sql = SqlHelper(table='test', opt_type=SqlHelper.opt_types['insert'] )
    sql.set_columns_and_values(columns=['name','age'], values=['zyd', 25])
    #sql.set_columns_and_values(values=['zyd', 25])
    sql.add_condition(key='sex', value=1)
    sql.get_sql()

    # test delete
    sql = SqlHelper(table='test', opt_type=SqlHelper.opt_types['delete'] )
    sql.set_columns_and_values(columns=['name','age'], values=['zyd', 25])
    sql.add_condition(key='sex', value=1)
    sql.add_conditions(['degree=1'])
    sql.get_sql()


    # test update
    sql = SqlHelper(table='test', opt_type=SqlHelper.opt_types['update'] )
    #sql.set_columns_and_values(columns=['name','age'], values=['zyd', 25])
    sql.add_keyValue(key='age', value=32)
    sql.add_keyValues(["name='zyd1'"])
    sql.add_condition(key='sex', value=1)
    sql.add_conditions(["degree=1"])
    sql.get_sql()

    # test select
    sql = SqlHelper(table='test', opt_type=SqlHelper.opt_types['select'] )
    #sql.set_columns_and_values(columns=['name','age'], values=None)
    sql.add_column('count(*)')
    #sql.add_keyValue(key='age', value=32)
    #sql.add_keyValues(["'name'='zyd1'"])
    sql.add_conditions(["degree=1"])
    sql.add_condition(key='sex', value=1)
    sql.set_sql_sub_script(' order by degree')



    sql.get_sql()