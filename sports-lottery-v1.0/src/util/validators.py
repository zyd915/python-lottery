#coding=UTF-8

__author__ = 'zhangyude'
from util.exceptions import *

class BaseValidator(object):
    compare = lambda self, a, b: a is not b
    clean = lambda self, x: x
    message = 'Ensure this value is %(limit_value)s (it is %(show_value)s).'
    code = 'limit_value'

    def __init__(self, limit_value):
        self.limit_value = limit_value

    def __call__(self, value):
        cleaned = self.clean(value)
        params = {'limit_value': self.limit_value, 'show_value': cleaned}
        if self.compare(cleaned, self.limit_value):
            raise ValidateError(
                self.message % params
            )


class MaxValueValidator(BaseValidator):
    compare = lambda self, a, b: a > b
    message = 'Ensure this value is less than or equal to %(limit_value)s.'
    code = 'max_value'


class MinValueValidator(BaseValidator):
    compare = lambda self, a, b: a < b
    message = 'Ensure this value is greater than or equal to %(limit_value)s.'
    code = 'min_value'


class MinLengthValidator(BaseValidator):
    compare = lambda self, a, b: a < b
    clean = lambda self, x: len(x)
    message = 'Ensure this value has at least %(limit_value)d characters (it has %(show_value)d).'
    code = 'min_length'


class MaxLengthValidator(BaseValidator):
    compare = lambda self, a, b: a > b
    clean = lambda self, x: len(x)
    message = 'Ensure this value has at most %(limit_value)d characters (it has %(show_value)d).'
    code = 'max_length'