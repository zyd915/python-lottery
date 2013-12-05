#coding=UTF-8
__author__ = 'Administrator'
from util.db.model.models import *
from util.db.db_util import *
import settings

class DBHelper(object):

    # 获取默认配置的数据库连接
    @staticmethod
    def get_default_conn():
        return db_conn(settings.db_file_path)

    # 执行SQL脚本（多条语句同时执行）
    @staticmethod
    def execute_by_sql_script(conn=None, sql_script=None):
        return execute_sql_script(conn=conn, sql_script=sql_script)

    # 执行sql
    @staticmethod
    def execute_by_sql(conn=None, sql=None, params=None):
        return execute_sql(conn=conn,sql=sql, params=params)

    # 查询一个
    @staticmethod
    def fetch_one_by_sql(conn=None, sql=None, params=None, ObjType=None):
        if ObjType is None:
            return None
        try:
            cursor = query_sql(conn=conn, sql=sql, params=params)
            if cursor is not None :
                obj = ObjType()
                row = cursor.fetchone()
                DBHelper.load_obj_field(row, obj)
            return obj
        except Exception as e:
            if settings.debug_flag:
                print(u'DBHelper.fetch_one_by_sql error:' + e.args[0])
            return None

    # 查询多个
    @staticmethod
    def fetch_list_by_sql(conn=None, sql=None, params=None, ObjType=None, size=None):
        if ObjType is None:
            return None
        try:
            cursor = query_sql(conn=conn, sql=sql, params=params)
            if cursor is not None and cursor.rowcount > 0:
                list = []
                rows = None
                if size is not None:
                    rows = cursor.fetchmany(size=size)
                else:
                    rows = cursor.fetchall()
                for row in rows:
                    obj = ObjType()
                    DBHelper.load_obj_field(row, obj)
                    list.append(obj)
            return list
        except Exception as e:
            if settings.debug_flag:
                print(u'DBHelper.fetch_list_by_sql error:' + e.args[0])
            return None

    # 加载obj的属性列表
    @staticmethod
    def load_fields_from_row(row=None, obj=None):
        if row is not None and len(row) > 0:
            for column in row.keys():
                if column in obj.__dict__ and isinstance(obj.__dict__[column], Field):
                    obj.__dict__[column].set_data_from_db(row[column])


    # 保存对象
    @staticmethod
    def save_obj(conn=None, obj=None):
        if obj is None or not isinstance(obj, Model):
            return exec_error
        tableName = obj._tableName
        dataItems = []
        columns_dict = obj.__dict__
        for column in columns_dict:
            field = columns_dict.get(column)
            if isinstance(field, Field):
                dataItems.append((column, field.data))
        return insert_data_one(obj.conn, tableName, dataItems)

    # 删除对象
    @staticmethod
    def delete_obj(conn=None, obj=None, by_primary_key=False):
        if obj is None or not isinstance(obj, Model):
            return exec_error
        tableName = obj._tableName or obj._name
        conditions = ""
        if by_primary_key:
            if obj._primaryKey is not None and obj.__dict__[obj._primaryKey] is not None:
                conditions = obj._primaryKey + '=' + obj.__dict__[obj._primaryKey].data
        else:
            fields = obj.get_fields()
            for name in fields :
                if fields[name] is None: continue
                condition = to_db_condition(name=name, value=fields[name])
                if condition is not None:
                    conditions += " " + condition + " and "
            conditions = conditions.rstrip(" and ")
        return delete_by_conditions(obj.conn, tableName, conditions)

    # 根据条件删除
    def deleteByConditions(conn=None,tableName=None, conditions=None, close_conn=False):
        try:
            return delete_by_conditions(conn=conn, tableName, conditions)
        finally:
            if close_conn:
                conn.close()

if  __name__ == '__main__':
    #DBHelper.insert_by_sql(conn=None, sql=None)
    dbhelper = DBHelper()
    #dbhelper.insert_by_sql(conn=None, sql=None)