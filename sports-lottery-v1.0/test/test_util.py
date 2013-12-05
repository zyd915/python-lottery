#coding=UTF-8
__author__ = 'Administrator'

def test_fun(fun, *args):
    if callable(fun):
        fun(args)

