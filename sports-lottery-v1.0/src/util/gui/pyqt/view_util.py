#coding=UTF-8

__author__ = 'zhangyude'

import sys
from PyQt5 import QtGui, QtCore

def view_center(uiObject):
    screen = QtGui.QDesktopWidget().screenGeometry()
    size = uiObject.geometry()
    uiObject.move((screen.width() - size.width())/2,(screen.height() - size.height())/2)

def view_show(UIObject):
    app = QtGui.QApplication(sys.argv)
    uiObject = UIObject()
    uiObject.show()
    sys.exit(app.exec_())
