# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(626, 452)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.comboBox = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox.setGeometry(QtCore.QRect(0, 10, 91, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.input_url = QtWidgets.QLineEdit(self.centralWidget)
        self.input_url.setEnabled(True)
        self.input_url.setGeometry(QtCore.QRect(90, 10, 291, 81))
        self.input_url.setObjectName("input_url")
        self.input_arg = QtWidgets.QLineEdit(self.centralWidget)
        self.input_arg.setGeometry(QtCore.QRect(492, 10, 121, 81))
        self.input_arg.setObjectName("input_arg")
        self.output = QtWidgets.QTextEdit(self.centralWidget)
        self.output.setGeometry(QtCore.QRect(10, 120, 611, 271))
        self.output.setObjectName("output")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralWidget)
        self.comboBox_2.setGeometry(QtCore.QRect(410, 10, 81, 21))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.startx = QtWidgets.QPushButton(self.centralWidget)
        self.startx.setGeometry(QtCore.QRect(410, 40, 81, 31))
        self.startx.setObjectName("startx")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 626, 22))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionabout_me = QtWidgets.QAction(MainWindow)
        self.actionabout_me.setObjectName("actionabout_me")
        self.menu.addAction(self.actionabout_me)
        self.menuBar.addAction(self.menu.menuAction())

        #ceshi
        # self.startx.
        #yishang

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "跨站辅助验证工具"))
        self.comboBox.setItemText(0, _translate("MainWindow", "目标URL："))
        self.output.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "参数"))
        self.startx.setText(_translate("MainWindow", "开始测试"))
        self.menu.setTitle(_translate("MainWindow", "关于"))
        self.actionabout_me.setText(_translate("MainWindow", "about me"))

if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    # w = QtWidgets.QWidget()
    # w.resize(400, 200)
    # w.setWindowTitle("hello PyQt5")
    # w.show()
    # exit(app.exec_())
    app2 = Ui_MainWindow()
    app2.setupUi()
    app2.retranslateUi()
