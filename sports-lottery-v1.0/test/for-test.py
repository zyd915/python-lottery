#coding=UTF-8
__author__ = 'Administrator'
def doFor():
    columms = ['name', 'age', 'sex']
    row = {'name':'zyd','age':12,'sex':1,'weight':65}
    for c in row.keys():
        for column in columms:
            if column == c:
                print(row[column])

if __name__ == '__main__':
    doFor()