#coding=UTF-8

__author__ = 'zhangyude'

import os
def ui2pyByFileZip(fileZip):
    res = 0
    for ui, py in fileZip:
        res = os.system('pyuic4 -o %s %s' % (py, ui))
        if res > 0:
            return res
    return res

def ui2pyByFileList(uiFileList, pyFileList):
    res = 0
    for ui, py in zip(uiFileList, pyFileList):
        res = os.system('pyuic4 -o %s %s' % (py, ui))
        if res > 0:
            return res
    return res


def ui2pyByFile(uiFile, pyFile):
    uiFile = uiFile.replace('\\', '/')
    pyFile = pyFile.replace('\\', '/')
    return os.system('pyuic4 -o %s %s' % (pyFile, uiFile))
