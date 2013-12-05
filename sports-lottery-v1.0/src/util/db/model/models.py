#coding=UTF-8

__author__ = 'zhangyude'
from util.db.model.fields import *
from util.db.db_util import *
from settings import *
from util.db.model.db_helper import *

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
            sql_create = 'create table ' + self._tableName + '(\n'
            fields = self.get_fields()
            for field in fields.values():
                sql_create += ' ' + field.get_create_field_sql() + ', \n'
            sql_create = sql_create.rstrip(', \n')
            sql_create += '\n) '
        return self.execute_by_sql(conn=self.conn, sql=sql_create)

    # 获取Model属性字典
    def get_fields(self, obj=None, fieldName=None):
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
                if isinstance(fields[field], Field):
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

    def save(self, close_conn=False):
        self.get_conn()
        try:
            return self.save_obj(conn=self.conn, obj=self)
        finally:
            self.close_conn(close_conn)

    def delete(self, close_conn=False, by_primary_key=False):
        self.get_conn()
        try:
            return self.delete_obj(conn=self.conn, obj=self, by_primary_key=by_primary_key)
        finally:
            self.close_conn(close_conn)



    def update(self, close_conn=False):
        self.get_conn()
        tableName = self._tableName or self._name
        conditions = None
        if self._primaryKey is not None and self.__dict__[self._primaryKey] is not None:
            conditions = self._primaryKey + '=' + self.__dict__[self._primaryKey].data
        dataItems = []
        columns_dict = self.__dict__
        for column in columns_dict:
            if isinstance(columns_dict.get(column), Field) and column is not self._primaryKey:
                dataItems.append((column, columns_dict.get(column).data))
        try:
            return update_by_conditions(self.conn, tableName, dataItems, conditions)
        finally:
            self.close_conn(close_conn)

    def updateByConditions(self, conditions, close_conn=False):
        self.get_conn()
        tableName = self._tableName or self._name
        dataItems = []
        columns_dict = self.__dict__
        for column in columns_dict:
            if isinstance(columns_dict.get(column), Field):
                dataItems.append((column, columns_dict.get(column).data))
        try:
            return update_by_conditions(self.conn, tableName, dataItems, conditions)
        finally:
            self.close_conn(close_conn)

    def loadDataByPrimaryValue(self, primaryValue=None, close_conn=False):
        self.get_conn()
        tableName = self._tableName or self._name
        conditions = None
        if self._primaryKey is not None and self.__dict__[self._primaryKey] is not None:
            conditions = self._primaryKey + '=' + primaryValue
        if conditions is not None:
            sql = u'select * from ' + tableName + u' where ' + conditions + u'limit 1'
            try:
                cursor = query_sql(self.conn, sql)
                if cursor is None:
                    return None
                elif len(cursor) > 0:
                    row = cursor[0]
                    self._loadFieldsValues(row)
            except:
                if debug_flag:
                    raise SqlError(u'加载数据出现异常')
                pass
        else:
            pass

    def _loadFieldsValues(self, row):
        for column in row.keys():
            self._loadFieldValue(column, row[column])

    def _loadFieldValue(self, column, data):
        if column is None or data is None:
            return
        if column in self.__dict__ and isinstance(self.__dict__[column], Field):
            self.__dict__[column].set_data_from_db(data)
