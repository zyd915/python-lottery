#coding=UTF-8

__author__ = 'zhangyude'
from util.db.model.fields import Field
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
                DBHelper.load_fields_from_row(row, obj)
                return obj
        except Exception as e:
            if settings.debug_flag:
                print(u'DBHelper.fetch_one_by_sql error:' + e.args[0])
            return None

    # 查询一个
    @staticmethod
    def fetch_one_by_obj_attributes(conn=None, obj=None):
        if obj is None or not isinstance(obj, Model):
            return None
        try:
            fields = obj.get_fields(justData=True, filterNone=True)
            sql_helper = SqlHelper(table=obj._tableName, opt_type=SqlHelper.opt_types['select'])
            if fields is not None and len(fields) > 0:
                for field in fields:
                    sql_helper.add_condition(key=field, value=fields[field])
            sql = sql_helper.get_sql()
            cursor = query_sql(conn=conn, sql=sql, params=None)
            if cursor is not None :
                row = cursor.fetchone()
                DBHelper.load_fields_from_row(row, obj)
                return obj
        except Exception as e:
            if settings.debug_flag:
                print(u'DBHelper.fetch_one_by_sql error:' + e.args[0])
            return None

    # 查询多个
    @staticmethod
    def fetch_list_by_obj_attributes(conn=None, obj=None, size=None):
        if obj is None or not isinstance(obj, Model):
            return None
        try:
            fields = obj.get_fields(justData=True, filterNone=True)
            sql_helper = SqlHelper(table=obj._tableName, opt_type=SqlHelper.opt_types['select'])
            if fields is not None and len(fields) > 0:
                for field in fields:
                    sql_helper.add_condition(key=field, value=fields[field])
            sql = sql_helper.get_sql()
            cursor = query_sql(conn=conn, sql=sql, params=None)
            if cursor is not None and cursor.rowcount > 0:
                list = []
                rows = None
                if size is not None:
                    rows = cursor.fetchmany(size=size)
                else:
                    rows = cursor.fetchall()
                for row in rows:
                    item = type(obj)()
                    DBHelper.load_fields_from_row(row, item)
                    list.append(item)
                return list
        except Exception as e:
            if settings.debug_flag:
                print(u'DBHelper.fetch_list_by_sql error:' + e.args[0])
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
                    DBHelper.load_fields_from_row(row, obj)
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
    def save_obj(conn=None, obj=None, conditions=None):
        if obj is None or not isinstance(obj, Model):
            return exec_error
        tableName = obj._tableName
        fieldList = obj.get_fields(justData=True, filterNone=True)
        return insert_one_by_dataDict_conditions(conn=obj.conn, tableName=tableName, dataDict=fieldList, conditions=conditions)

    # 删除对象
    @staticmethod
    def delete_obj(conn=None, obj=None, by_primary_key=False):
        if obj is None or not isinstance(obj, Model):
            return exec_error
        tableName = obj._tableName
        conditions = ""
        if by_primary_key:
            if obj._primaryKey is not None and obj.__dict__[obj._primaryKey] is not None:
                conditions = obj._primaryKey + '=' + obj.__dict__[obj._primaryKey].data
        else:
            fields = obj.get_fields(justData=True, filterNone=True)
            for name in fields :
                if fields[name] is None: continue
                condition = to_db_condition(name=name, value=fields[name])
                if condition is not None:
                    conditions += " " + condition + " and "
            conditions = conditions.rstrip(" and ")
        return delete_by_conditions(conn=conn, tableName=tableName, conditions=conditions)

    # 根据条件删除
    @staticmethod
    def delete_by_conditions(conn=None,tableName=None, conditions=None, close_conn=False):
        try:
            return delete_by_conditions(conn=conn, tableName=tableName, conditions=conditions)
        finally:
            if close_conn:
                conn.close()

    # 更新
    @staticmethod
    def update_obj(conn=None, obj=None, conditions=None, by_primary_key=False):
        if obj is None :
            return exec_error
        if not by_primary_key and conditions is None:
            conditions = '1=1'
        conditions = conditions
        if isinstance(obj, Model) and by_primary_key:
            if obj._primaryKey is None or obj.__dict__[obj._primaryKey] is None:
                return exec_error
            conditions = obj._primaryKey + '=' + obj.__dict__[obj._primaryKey].data
        elif isinstance(obj, Model) and not by_primary_key:
            fields = obj.get_fields(justData=True, filterNone=True)
        return update_by_conditions(conn=conn, tableName=obj._tableName, dataDict=fields, conditions=conditions)


# 模型基类
class Model(DBHelper):

    # 初始化函数
    def __init__(self, _name=None, _tableName=None, _primaryKey=None, _columns=[], _sql_create=None):
        self._name = _name
        self._tableName = _tableName or _name
        self._primaryKey = _primaryKey
        self._columns = _columns
        self._sql_create = _sql_create
        self.conn = None

    def __eq__(self, other):
        if other is None or not isinstance(other, self.__class__):
            return False
        elif other._tableName is not None and other._tableName == self._tableName:
            return self.get_fields(obj=other,fieldName=self._primaryKey).data == self.get_fields(fieldName=self._primaryKey).data
        else:
            return False

    # 通过model实例创建表
    def db_create_table(self):
        self.get_conn()
        sql_create = None
        if self._sql_create is not None:
            sql_create = self._sql_create
        else:
            sql_create = u'create table ' + self._tableName + '(\n'
            fields = self.get_fields()
            for field in fields.values():
                sql_create += ' ' + field.get_create_field_sql() + ', \n'
            sql_create = sql_create.rstrip(', \n')
            sql_create += '\n) '
        return self.execute_by_sql(conn=self.conn, sql=sql_create)

    # 获取Model属性字典
    def get_fields(self, obj=None, fieldName=None,justData=False, filterNone=False, filterPrimaryKey=False):
        object = None
        if obj is None:
            object = self
        elif obj is not None and isinstance(obj, Model):
            object = obj
        fields = object.__dict__
        if fieldName is not None:
            if fieldName in fields and isinstance(fields[fieldName], Field):
                return fields[fieldName]
            else:
                return None
        else:
            fieldList = {}
            for field in fields:
                if isinstance(fields[field], Field) :
                    if filterPrimaryKey and field == object._primaryKey:
                        continue
                    if justData:
                        if filterNone and fields[field].data is None:
                            continue
                        fieldList[field] = fields[field].data
                    else:
                        fieldList[field] = fields[field]

            return fieldList

    # 获取数据库连接
    def get_conn(self):
        if self.conn is None:
            self.conn = self.get_default_conn()
        return self.conn

    # 设置数据库连接
    def set_conn(self, conn):
        self.conn = conn

    # 关闭数据库连接
    def close_conn(self, close=False):
        if self.conn is not None and close is True:
            self.conn.close()

    # 加载列名
    def load_columns(self):
        columns_dict = self.__dict__
        for column in columns_dict:
            if isinstance(columns_dict.get(column), Field):
                self._columns.append(column)
        return self._columns

    def save(self, close_conn=False, conditions=None):
        self.get_conn()
        try:
            return self.save_obj(conn=self.conn, obj=self, conditions=conditions)
        finally:
            self.close_conn(close_conn)

    def delete(self, close_conn=False, by_primary_key=False):
        self.get_conn()
        try:
            return self.delete_obj(conn=self.conn, obj=self, by_primary_key=by_primary_key)
        finally:
            self.close_conn(close_conn)



    def update(self, conditions=None, close_conn=False):
        self.get_conn()
        try:
            return self.update_obj(conn=self.conn, obj=self, conditions=conditions)
        finally:
            self.close_conn(close_conn)

