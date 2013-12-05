#coding=UTF-8
__author__ = 'Administrator'

def printTry():
    a = ''
    try:
        a = 'try'
        #raise ValueError
        return a
    except Exception as e:
        return 'exception'
    else:
       print('else')
    finally:
       print('finally')

if __name__ == '__main__':
    debug = False
    if debug:
        print(printTry())