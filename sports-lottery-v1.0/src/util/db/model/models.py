#coding=UTF-8

__author__ = 'zhangyude'
from util.db.model.fields import Field
from util.db.model.db_helper import DBHelper

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



    def update(self, conditions=None, close_conn=False):
        self.get_conn()
        try:
            return self.update_obj(conn=self.conn, obj=self, conditions=conditions)
        finally:
            self.close_conn(close_conn)

