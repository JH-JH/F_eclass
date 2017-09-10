# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(460, 248)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(110, 90, 56, 20))
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(110, 120, 56, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.userID = QtWidgets.QLineEdit(Dialog)
        self.userID.setGeometry(QtCore.QRect(170, 90, 113, 20))
        self.userID.setObjectName("userID")
        self.userPW = QtWidgets.QLineEdit(Dialog)
        self.userPW.setGeometry(QtCore.QRect(170, 120, 113, 20))
        self.userPW.setObjectName("userPW")
        self.LoginButton = QtWidgets.QPushButton(Dialog)
        self.LoginButton.setGeometry(QtCore.QRect(290, 120, 75, 23))
        self.LoginButton.setObjectName("LoginButton")

        self.retranslateUi(Dialog)
        self.LoginButton.clicked['bool'].connect(Dialog.LoginClicked)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "ID:"))
        self.label_2.setText(_translate("Dialog", "PW:"))
        self.LoginButton.setText(_translate("Dialog", "Login"))


class Action_Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

    def LoginClicked(self):
        global app, Dialog
        if self.ui.userID.text() != "" and self.ui.userPW.text() != "":
            print(self.ui.userID.text(), self.ui.userPW.text())
            app.exit()

            Dialog = Action_Main()
            Dialog.ui = Ui_Main()
            Dialog.ui.setupUi(Dialog)
            Dialog.show()
        else:
            print(" > ID와 PW를 입력해주세요!")


class Ui_Main(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(803, 576)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 321, 231))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.L_Class = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.L_Class.setObjectName("L_Class")
        self.verticalLayout.addWidget(self.L_Class)
        self.L_Category1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.L_Category1.setObjectName("L_Category1")
        self.verticalLayout.addWidget(self.L_Category1)
        self.L_Category1_1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.L_Category1_1.setObjectName("L_Category1_1")
        self.verticalLayout.addWidget(self.L_Category1_1)
        self.L_Category1_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.L_Category1_2.setObjectName("L_Category1_2")
        self.verticalLayout.addWidget(self.L_Category1_2)
        self.L_Category1_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.L_Category1_3.setObjectName("L_Category1_3")
        self.verticalLayout.addWidget(self.L_Category1_3)
        self.L_Category1_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.L_Category1_4.setObjectName("L_Category1_4")
        self.verticalLayout.addWidget(self.L_Category1_4)
        self.L_Category2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.L_Category2.setObjectName("L_Category2")
        self.verticalLayout.addWidget(self.L_Category2)
        self.L_Category2_1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.L_Category2_1.setObjectName("L_Category2_1")
        self.verticalLayout.addWidget(self.L_Category2_1)
        self.L_Category2_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.L_Category2_2.setObjectName("L_Category2_2")
        self.verticalLayout.addWidget(self.L_Category2_2)
        self.L_Category2_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.L_Category2_3.setObjectName("L_Category2_3")
        self.verticalLayout.addWidget(self.L_Category2_3)
        self.L_Category2_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.L_Category2_4.setObjectName("L_Category2_4")
        self.verticalLayout.addWidget(self.L_Category2_4)

        self.retranslateUi(Dialog)
        self.L_Class.linkActivated['QString'].connect(Dialog.open)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Main-Eclass"))
        self.L_Class.setText(_translate("Dialog", "Class"))
        self.L_Category1.setText(_translate("Dialog", "Category"))
        self.L_Category1_1.setText(_translate("Dialog", "content"))
        self.L_Category1_2.setText(_translate("Dialog", "content"))
        self.L_Category1_3.setText(_translate("Dialog", "content"))
        self.L_Category1_4.setText(_translate("Dialog", "content"))
        self.L_Category2.setText(_translate("Dialog", "Category"))
        self.L_Category2_1.setText(_translate("Dialog", "content"))
        self.L_Category2_2.setText(_translate("Dialog", "content"))
        self.L_Category2_3.setText(_translate("Dialog", "content"))
        self.L_Category2_4.setText(_translate("Dialog", "content"))


class Action_Main(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

    def open(self):
        global app
        # if self.ui.userID.text() != "" and self.ui.userPW.text() != "":
        print(self.ui.L_Class.text())
        #    app.exit()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = Action_Login()
    Dialog.ui = Ui_Login()
    Dialog.ui.setupUi(Dialog)
    Dialog.show()
    app.exec_() #for LoginDialog
    app.exec_() #for MainDialog

