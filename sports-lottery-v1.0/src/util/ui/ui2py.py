#coding=UTF-8

__author__ = 'zhangyude'

from PyQt5 import QtGui, QtCore
import util.gui.pyqt.view_util as view_util
import util.gui.pyqt.table_util as table_util
import util.ui.ui_util as ui_util

class Ui2Py(QtGui.QMainWindow):
    def __init__(self):
        super(Ui2Py,self).__init__()
        self.initUI()
        view_util.view_center(self)

    def initUI(self):
        self.content = QtGui.QWidget(self)

        hBoxLayout = QtGui.QHBoxLayout(self.content)

        # 顶部左边
        self.topLeftGroup = QtGui.QGroupBox(u'选择UI', self)
        self.topLeftGroup.setMaximumWidth(350)
        self.initTopLeftGroup()

        # 顶部右边
        self.topRightGroup = QtGui.QGroupBox(u'UI列表', self)
        self.initTopRightGroup()

        # 底部
        self.bottomGroup = QtGui.QGroupBox(u'生成文件列表', self)
        self.bottomGroup.setFixedHeight(300)
        self.initBottomGroup()

        # 分隔栏1
        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(self.topLeftGroup)
        splitter1.addWidget(self.topRightGroup)

        # 分隔栏2
        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.bottomGroup)

        hBoxLayout.addWidget(splitter2)
        self.content.setLayout(hBoxLayout)

        self.setCentralWidget(self.content)
        # 设置窗体背景颜色
        self.content.setStyleSheet('QWidget {background-color : %s}' % QtGui.QColor(QtCore.Qt.white).name())
        # 设置分隔栏中的托手
        # QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        self.setFixedSize(800,500)
        self.setWindowTitle('UI2PY')

    # 初始化顶部左边的group
    def initTopLeftGroup(self):
        grid = QtGui.QGridLayout()
        labelFileType = QtGui.QLabel()
        labelFileType.setText(u'文件类型：')

        labelUiPath = QtGui.QLabel()
        labelUiPath.setText(u'文件目录：')

        labelPyPath = QtGui.QLabel()
        labelPyPath.setText(u'保存目录：')

        self.fileType = self.createComboBox(['*.ui'])
        self.fileType.setFixedHeight(25)

        self.uiPath = self.createComboBox([QtCore.QDir.currentPath()])
        self.uiPath.setFixedHeight(25)
        self.uiPath.currentIndexChanged.connect(lambda : self.insertUIFileItem(self.uiPath.currentText()))

        self.pyPath = self.createComboBox([QtCore.QDir.currentPath()])
        self.pyPath.setFixedHeight(25)

        btnOpenUiPath = self.createButton(u'浏览', self.selectDirPath, self.uiPath)
        btnOpenPyPath = self.createButton(u'浏览', self.selectDirPath, self.pyPath)
        btnCreatePyFile = self.createButton(u'生成', self.createPyFile, None)
        btnResetConfig = self.createButton(u'重置', self.cleanUIList, None)

        optWidget = QtGui.QWidget()
        optLayout = QtGui.QHBoxLayout()
        leftSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        rightSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        optLayout.addSpacerItem(leftSpacer)
        optLayout.addWidget(btnCreatePyFile)
        optLayout.addWidget(btnResetConfig)
        optLayout.addSpacerItem(rightSpacer)
        optWidget.setLayout(optLayout)

        grid.addWidget(labelFileType, 0,0)
        grid.addWidget(self.fileType,0,1,1,2)
        grid.addWidget(labelUiPath,1,0)
        grid.addWidget(self.uiPath,1,1)
        grid.addWidget(btnOpenUiPath,1,2)
        grid.addWidget(labelPyPath,2,0)
        grid.addWidget(self.pyPath,2,1)
        grid.addWidget(btnOpenPyPath,2,2)
        grid.addWidget(optWidget, 3,0,1,3)

        self.topLeftGroup.setLayout(grid)

    # 初始化顶部右边的group
    def initTopRightGroup(self):
        model = QtGui.QStandardItemModel(0, 2, self.topRightGroup)
        headers = [u'UI文件', u'py文件（可编辑）']
        headerRoles = [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]
        table_util.initModelHeader(model, headers, headerRoles)
        self.uiListView = table_util.createTreeView(model)
        self.uiListView.setReadOnlyColumns([0])
        self.uiListView.setDataChangedValidateHandler(self.renamePyFileNameValidateHandler)
        # self.insertUIFileItem()
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.uiListView)
        self.topRightGroup.setLayout(layout)

    def initBottomGroup(self):
        model = QtGui.QStandardItemModel(0, 1, self.bottomGroup)
        headers = [u'生成的py文件']
        headerRoles = [QtCore.Qt.DisplayRole]
        table_util.initModelHeader(model, headers, headerRoles)
        self.pyListView = table_util.createTreeView(model)
        self.pyListView.setReadOnlyColumns([0])
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.pyListView)
        self.bottomGroup.setLayout(layout)

    # 重命名py文件名验证
    def renamePyFileNameValidateHandler(self, index_new, index_old):
        pyFileName = index_new.data().toString()
        column = index_new.column()
        oldData = index_old.data()
        if not pyFileName.endsWith(QtCore.QString('.py')) and column not in self.uiListView.readOnlyColumns and oldData is not None:
            QtGui.QMessageBox.warning (self, u'提示', u'文件名以.py结尾', u'好', '', '', 0, -1)

    # 向UI列表中插入item
    def insertUIFileItem(self, path):
        if self.pyPath.findText(path) == -1:
            self.pyPath.addItem(path)
        self.pyPath.setCurrentIndex(self.pyPath.findText(path))
        model = self.uiListView.model()
        table_util.clearModelData(model)
        uiDir = QtCore.QDir(path)
        uiDir.setNameFilters(QtCore.QStringList('*.ui'))
        if uiDir.exists():
            fileList = uiDir.entryInfoList()
            for file in fileList:
                uiFileName = file.fileName()
                if uiFileName.endsWith('.ui', QtCore.Qt.CaseInsensitive):
                    pyFileName = uiFileName.left(uiFileName.lastIndexOf('.', -1, QtCore.Qt.CaseInsensitive)).append('.py')
                    table_util.insertModelData(model, [uiFileName, pyFileName])



    # 生成py文件
    def createPyFile(self):
        uiFileList = []
        pyFileList = []
        uiModel = self.uiListView.model()
        rowCount = uiModel.rowCount()
        for rowNum in range(rowCount):
            uiName = uiModel.item(rowNum, 0).text()
            pyName = uiModel.item(rowNum, 1).text()
            uiFileList.append(uiName)
            pyFileList.append(pyName)

        uiPath = self.uiPath.currentText()
        pyPath = self.pyPath.currentText()

        createdPyList = []
        for ui, py in zip(uiFileList, pyFileList):
            uiFile = uiPath.append('/').append(ui)
            pyFile = pyPath.append('/').append(py)
            if ui_util.ui2pyByFile(uiFile, pyFile) > 0:
                QtGui.QMessageBox.warning (self, u'提示', u'生成UI：%s 发生异常！' % uiFile, u'好', '', '', 0, -1)
            else:
                createdPyList.append(pyFile)
        self.insertPyFileItem(createdPyList)

    # 向py列表中插入item
    def insertPyFileItem(self, createdPyList):
        model = self.pyListView.model()
        table_util.clearModelData(model)
        for py in createdPyList:
            table_util.insertModelData(model, [py])


    # 重置
    def cleanUIList(self):
        model = self.uiListView.model()
        table_util.clearModelData(model)

    # 找到路径
    def selectDirPath(self, pathCombo):
        path = QtGui.QFileDialog.getExistingDirectory(self, u"选择目录", QtCore.QDir.currentPath())
        if path :
            if pathCombo.findText(path) == -1:
                pathCombo.addItem(path)
            pathCombo.setCurrentIndex(pathCombo.findText(path))

    # 创建按钮
    def createButton(self, text, clickEventHandler, params):
        button = QtGui.QPushButton(text)
        if params is None:
            button.clicked.connect(lambda : clickEventHandler())
        else:
            button.clicked.connect(lambda : clickEventHandler(params))
        return button

    # 创建复选框
    def createComboBox(self, text = []):
        comboBox = QtGui.QComboBox()
        comboBox.setEditable(True)
        comboBox.addItems(text)
        comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        return comboBox

# 显示界面
view_util.view_show(Ui2Py)