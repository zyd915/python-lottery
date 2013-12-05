#coding=UTF-8

__author__ = 'zhangyude'
import sys
from PyQt5 import QtGui, QtCore, QtSql

class TableMode():
    QAbstractListModel = QtCore.QAbstractListModel
    QAbstractProxyModel = QtGui.QAbstractProxyModel
    QAbstractTableModel = QtCore.QAbstractTableModel
    QDirModel = QtGui.QDirModel
    QFileSystemModel = QtGui.QFileSystemModel

    QProxyModel =  QtGui.QProxyModel
    QStandardItemModel = QtGui.QStandardItemModel
    QStringListModel = QtGui.QStringListModel

    QSortFilterProxyModel = QtGui.QSortFilterProxyModel

    QItemSelectionModel = QtGui.QItemSelectionModel

    QSqlQueryModel = QtSql.QSqlQueryModel
    QSqlTableModel = QtSql.QSqlTableModel
    QSqlRelationalTableModel = QtSql.QSqlRelationalTableModel

class TreeView(QtGui.QTreeView):

    def __init__(self):
        super(TreeView, self).__init__()
        self.connect(self, QtCore.SIGNAL('clicked(QModelIndex)'), self.clickedProxy)
        self.setSelectionBehavior(self.SelectItems)
        self.setEditTriggers(self.SelectedClicked)

    def dataChanged(self, index_old, index_new):
        if hasattr(self, 'dataChangedValidateHandler') and self.dataChangedValidateHandler is not None:
            self.dataChangedValidateHandler(index_new, index_old)

    def setDataChangedValidateHandler(self, handler):
        self.dataChangedValidateHandler = handler

    def setReadOnlyColumns(self, columns):
        self.readOnlyColumns = columns

    def clickedProxy(self, index):
        column = index.column()
        if len(self.readOnlyColumns) > 0 and column in self.readOnlyColumns:
            self.clearSelection()
            pass
        else:
            self.clicked()


def createTableView(model):
    view = QtGui.QTableView()
    view.setModel(model)
    return view

def createTreeView(model):
    view = QtGui.QTreeView()
    view.setRootIsDecorated(False)
    view.setAlternatingRowColors(True)
    view.setModel(model)
    return view

def createTreeView(model):
    view = TreeView()
    view.setRootIsDecorated(False)
    view.setAlternatingRowColors(True)
    view.setModel(model)
    return view

def initModelHeader(model, headers):
    for i in range(len(headers)) :
        model.setHeaderData(i, QtCore.Qt.Horizontal, headers[i])
    model.select()

def initModelHeader(model, headers, headerRoles):
    for i in range(len(headers)) :
        model.setHeaderData(i, QtCore.Qt.Horizontal, headers[i], headerRoles[i])


def insertModelData(model, columnDataSet):
    model.insertRow(0)
    for i in range(len(columnDataSet)):
        model.setData(model.index(0,i), columnDataSet[i], QtCore.Qt.DisplayRole)

def clearModelData(model):
    startRowNum = 0;
    endRowNum = model.rowCount()
    model.removeRows(startRowNum, endRowNum)
