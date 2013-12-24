#coding=UTF-8
__author__ = 'Administrator'

import datetime
import decimal

from util.exceptions import *
from util.validators import *


date_fmt_str = 'yyyy-MM-dd'
datetime_fmt_str = 'yyyy-MM-dd HH:mm:ss'
key_field_value = 'field_value'
key_field_type = 'field_type'

def get_type_value_dic(type, value):
    return {key_field_type:type, key_field_value:value}

class Field(object):

    default_error_msg = {
        'transfer_to_python': 'The value(%(field_value)) transfer to %(field_type) error '
    }
    def __init__(self,
                 name = None,
                 comment = None,
                 primaryKey = False,
                 data = None,
                 default = None,
                 maxLength = None,
                 unique = False,
                 blank = True,
                 auto = False,
                 column = None,
                 tablespace = None,
                 validators = [],
                 error_msg = None
                 ):
        self.name = name
        self.comment = comment
        self.primaryKey = primaryKey
        self.data = data
        self.default = default
        self.maxLength = maxLength
        self.unique = unique
        self.blank = blank
        self.auto = auto
        self.column = name or column
        self.tablespace = tablespace
        self.validators = validators
        self.error_msg = error_msg

    def to_python(self, value):
        return value

    def get_type(self):
        return self.__class__.__name__

    def get_name_column(self):
        return (self.name, self.column)

    def get_default(self):
        if self.default is not None:
            if callable(self.default):
                return self.default()
            return self.default
        return None

    def set_data_from_db(self, data):
        self.data = self.to_python(data)

    def get_create_field_sql(self):
        return ""

# 布尔类型
class BooleanField(Field):

    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        if 'default' not in kwargs and not kwargs.get('null'):
            kwargs['default'] = False
        Field.__init__(self, *args, **kwargs)

    def get_type(self):
        return 'BooleanField'

    def to_python(self, value):
        if value in (True, False):
            return bool(value)
        elif value in ('true', 'True', 1):
            return True
        elif value in ('false', 'False', 0):
            return False
        else:
            msg = Field.default_error_msg['transfer_to_python'] % get_type_value_dic(self.get_type(),value)
            raise ValidateError(msg)

    def get_create_field_sql(self):
        sql = self.column + " integer "
        if self.default is not None and isinstance(self.default, bool):
            sql += " default " + int(self.default)

# 字符串类型
class CharField(Field):
    
    def __init__(self, *args, **kwargs):
        super(CharField, self).__init__(*args, **kwargs)
        self.validators.append(MaxLengthValidator)

    def get_type(self):
        return 'CharField'

    def to_python(self, value):
        try:
            if isinstance(value, str) or value is None:
                return value
            else:
                return str(value, "utf-8")
        except Exception as e:
            msg = Field.default_error_msg['transfer_to_python'] % get_type_value_dic(self.get_type(),value)
            raise ValidateError(msg)

    def get_create_field_sql(self):
        sql = self.column + " text "
        if self.default is not None and isinstance(self.default, str):
            sql += " default " + str(self.default)
        if not self.blank :
            sql += ' not null '
        if self.unique :
            sql += ' unique '
        return sql

# 日期类型
class DateField(Field):
    def __init__(self, auto=False, **kwargs):
        if auto is True:
            self.data = datetime.date()
        super.__init__(self, auto=auto, **kwargs)

    def get_type(self):
        return 'DateField'

    def to_python(self, value):
        try:
            if isinstance(value, datetime.date) or value is None:
                return value
            elif isinstance(value, datetime.datetime):
                return value.date()
            elif isinstance(value, str):
                return datetime.datetime.strptime(value, date_fmt_str)
        except Exception as e:
            msg = Field.default_error_message['invalid'] % get_type_value_dic(self.get_type(),value)
            raise ValidateError(msg)

    def get_create_field_sql(self):
        sql = self.column + " date "
        if self.default is not None and isinstance(self.default, datetime.date):
            sql += " default " + str(self.default)
        if not self.blank :
            sql += ' not null '
        return sql

#时间类型
class DateTimeField(Field):
    def __init__(self, auto=False, **kwargs):
        if auto is True:
            self.data = datetime.datetime()
        super.__init__(self, auto=auto, **kwargs)

    def get_type(self):
        return 'DateTimeField'

    def to_python(self, value):
        try:
            if isinstance(value, datetime.datetime) or value is None:
                return value
            elif isinstance(value, datetime.date):
                return datetime.datetime(value.year, value.month, value.day)
            elif isinstance(value, str):
                return datetime.datetime.strptime(value, datetime_fmt_str)
        except Exception as e:
            msg = Field.default_error_message['invalid'] % get_type_value_dic(self.get_type(),value)
            raise ValidateError(msg)

    def get_create_field_sql(self):
        sql = self.column + " datetime "
        if self.default is not None and isinstance(self.default, datetime.datetime):
            sql += " default " + str(self.default)
        if not self.blank :
            sql += ' not null '
        return sql
#整型
class IntegerField(Field):

    def __init__(self, *args, **kwargs):
        super(IntegerField, self).__init__(*args, **kwargs)

    def get_type(self):
        return 'IntegerField'

    def to_python(self, value):
        try:
            if isinstance(value, int) or value is None:
                return value
            else:
                return int(value)
        except Exception as e:
            msg = Field.default_error_message['invalid'] % get_type_value_dic(self.get_type(),value)
            raise ValidateError(msg)

    def get_create_field_sql(self):
        sql = self.column + " integer "
        if self.primaryKey:
            sql += " primary key "
        else:
            if self.unique :
                sql += ' unique '
            if not self.blank :
                sql += ' not null '
            if self.default is not None and isinstance(self.default, int):
                sql += " default " + int(self.default)
        return sql
#浮点型
class FloatField(Field):

    def __init__(self, *args, **kwargs):
        super.__init__(self, *args, **kwargs)
    def get_type(self):
        return 'FloatField'

    def to_python(self, value):
        try:
            if isinstance(value, float) or value is None:
                return value
            else:
                return float(value)
        except Exception as e:
            msg = Field.default_error_message['invalid'] % get_type_value_dic(self.get_type(),value)
            raise ValidateError(msg)

    def get_create_field_sql(self):
        sql = self.column + " float "
        if self.default is not None and isinstance(self.default, float):
            sql += " default " + float(self.default)
        if not self.blank :
            sql += ' not null '
        if self.unique :
            sql += ' unique '
        return sql

#decimal类型
class DecimalField(Field):
    def __init__(self, p=10,s=0, **kwargs):
        self.p = p
        self.s = s
        super.__init__(self, **kwargs)

    def get_type(self):
        return 'DecimalField'

    def to_python(self, value):
        try:
            if isinstance(value, decimal.Decimal) or value is None:
                return value
            else:
                return decimal.Decimal(value)
        except Exception as e:
            msg = Field.default_error_message['invalid'] % get_type_value_dic(self.get_type(),value)
            raise ValidateError(msg)

    def get_create_field_sql(self):
        sql = self.column + ' decimal(' +self.p+','+self.s+') '
        if self.default is not None and isinstance(self.default, float):
            sql += " default " + float(self.default)
        if not self.blank :
            sql += ' not null '
        if self.unique :
            sql += ' unique '
        return sql