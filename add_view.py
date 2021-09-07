# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_add_view(object):
    def setupUi(self, add_view):
        add_view.setObjectName("add_view")
        add_view.setWindowModality(QtCore.Qt.ApplicationModal)
        add_view.resize(950, 560)
        add_view.setAutoFillBackground(False)
        add_view.setStyleSheet("QDialog{\n"
"background-color:#dedede;\n"
"}\n"
"QTableView , QListView{\n"
"padding:10px;\n"
"background-color:white;\n"
"border-radius:20px;\n"
"border:2px solid black;\n"
"}\n"
"QPushButton{\n"
"background-color:#2f419b;\n"
"border-radius:25px;\n"
"color:white;\n"
"}\n"
"QPushButton#btn_tak_of,#btn_sheet,#btn_line{\n"
"background-color:#2f419b;\n"
"border-radius:15px;\n"
"color:white;\n"
"}\n"
"QPushButton#btn_tak_of:hover,#btn_sheet:hover,#btn_line:hover{\n"
"background-color:rgb(55, 76, 182);\n"
"color:white;\n"
"}\n"
"QPushButton:hover{\n"
"background-color:rgb(55, 76, 182);\n"
"color:white;\n"
"}\n"
"QProgressBar:horizontal {\n"
"border: 1px solid rgba(255, 255, 255, 0);\n"
"border-radius: 2px;\n"
"background: #dedede;\n"
"padding:3px;\n"
"text-align:left;\n"
"margin-left:30px;\n"
"}\n"
"QProgressBar::chunk:horizontal {\n"
"background:  #2f419b;\n"
"border-radius:6px;\n"
"}")
        # add_view.setSizeGripEnabled(True)
        # add_view.setModal(False)
        self.frame = QtWidgets.QFrame(add_view)
        self.frame.setGeometry(QtCore.QRect(20, 20, 911, 391))
        self.frame.setAutoFillBackground(False)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.table_tak_of = QtWidgets.QTableView(self.frame)
        self.table_tak_of.setGeometry(QtCore.QRect(260, 60, 631, 311))
        self.table_tak_of.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_tak_of.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.table_tak_of.setObjectName("table_tak_of")
        self.table_tak_of.verticalHeader().setVisible(False)
        self.btn_line = QtWidgets.QPushButton(self.frame)
        self.btn_line.setGeometry(QtCore.QRect(640, 20, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.btn_line.setFont(font)
        self.btn_line.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_line.setObjectName("btn_line")
        self.btn_sheet = QtWidgets.QPushButton(self.frame)
        self.btn_sheet.setGeometry(QtCore.QRect(510, 20, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.btn_sheet.setFont(font)
        self.btn_sheet.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_sheet.setObjectName("btn_sheet")
        self.btn_tak_of = QtWidgets.QPushButton(self.frame)
        self.btn_tak_of.setGeometry(QtCore.QRect(400, 20, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.btn_tak_of.setFont(font)
        self.btn_tak_of.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_tak_of.setStyleSheet("background-color:#dedede;\n"
"        border:2px solid #2f419b;\n"
"        color:#2f419b;")
        self.btn_tak_of.setObjectName("btn_tak_of")
        self.table_sheet = QtWidgets.QTableView(self.frame)
        self.table_sheet.setGeometry(QtCore.QRect(260, 60, 631, 311))
        self.table_sheet.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_sheet.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.table_sheet.setGridStyle(QtCore.Qt.SolidLine)
        self.table_sheet.setObjectName("table_sheet")
        self.table_sheet.verticalHeader().setVisible(False)
        self.table_line = QtWidgets.QTableView(self.frame)
        self.table_line.setGeometry(QtCore.QRect(260, 60, 631, 311))
        self.table_line.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.table_line.setDragDropOverwriteMode(False)
        self.table_line.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_line.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.table_line.setShowGrid(True)
        self.table_line.setGridStyle(QtCore.Qt.SolidLine)
        self.table_line.setObjectName("table_line")
        self.table_line.verticalHeader().setVisible(False)
        self.listView = QtWidgets.QListWidget(self.frame)
        self.listView.setGeometry(QtCore.QRect(25, 60, 231, 311))
        self.listView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listView.setObjectName("listView")
        self.progressBar = QtWidgets.QProgressBar(add_view)
        self.progressBar.setGeometry(QtCore.QRect(70, 500, 811, 20))
        self.progressBar.setStyleSheet("")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.btn_delete = QtWidgets.QPushButton(add_view)
        self.btn_delete.setEnabled(False)
        self.btn_delete.setGeometry(QtCore.QRect(410, 420, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.btn_delete.setFont(font)
        self.btn_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete.setObjectName("btn_delete")
        self.btn_start = QtWidgets.QPushButton(add_view)
        self.btn_start.setEnabled(False)
        self.btn_start.setGeometry(QtCore.QRect(550, 420, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.btn_start.setFont(font)
        self.btn_start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_start.setObjectName("btn_start")
        self.btn_load = QtWidgets.QPushButton(add_view)
        self.btn_load.setGeometry(QtCore.QRect(270, 420, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.btn_load.setFont(font)
        self.btn_load.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_load.setObjectName("btn_load")

        self.retranslateUi(add_view)
        QtCore.QMetaObject.connectSlotsByName(add_view)

    def retranslateUi(self, add_view):
        _translate = QtCore.QCoreApplication.translate
        add_view.setWindowTitle(_translate("add_view", "Dialog"))
        self.btn_line.setText(_translate("add_view", "Line"))
        self.btn_sheet.setText(_translate("add_view", "Sheet"))
        self.btn_tak_of.setText(_translate("add_view", "Tak_of"))
        self.btn_delete.setText(_translate("add_view", "Delete Item"))
        self.btn_start.setText(_translate("add_view", "Start"))
        self.btn_load.setText(_translate("add_view", "Load PDF"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    add_view = QtWidgets.QDialog()
    ui = Ui_add_view()
    ui.setupUi(add_view)
    add_view.show()
    sys.exit(app.exec_())

