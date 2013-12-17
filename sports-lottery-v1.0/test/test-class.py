#coding=UTF-8
__author__ = 'Administrator'

class A(object):
    def __init__(self, name=None, age=None):
        self.name = name
        self.age = age

    def print_out(self):
        print('name: '+ self.name + ' age: '+ str(self.age))

if __name__ == '__main__':
    a = A()
    aa = type(a)(name='zyd', age=12)
    aa.print_out()