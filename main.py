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
        self.userPW.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
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
        Dialog.setEnabled(True)
        Dialog.resize(1086, 819)
        Dialog.setAutoFillBackground(False)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 781, 681))
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.Class1 = QtWidgets.QWidget()
        self.Class1.setObjectName("Class1")
        self.treeWidget = QtWidgets.QTreeWidget(self.Class1)
        self.treeWidget.setGeometry(QtCore.QRect(10, 10, 761, 641))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.treeWidget.setFont(font)
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.treeWidget.setAcceptDrops(False)
        self.treeWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.treeWidget.setAutoFillBackground(False)
        self.treeWidget.setInputMethodHints(QtCore.Qt.ImhNone)
        self.treeWidget.setAnimated(False)
        self.treeWidget.setAllColumnsShowFocus(False)
        self.treeWidget.setHeaderHidden(False)
        #self.treeWidget.setExpandsOnDoubleClick(False)

        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0.setExpanded(True)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0.setExpanded(True)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0.setExpanded(True)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.treeWidget.header().setCascadingSectionResizes(True)
        self.treeWidget.header().resizeSection(0,400)
        self.treeWidget.header().setMinimumSectionSize(300)
        self.treeWidget.header().setHighlightSections(True)
        self.treeWidget.header().setSortIndicatorShown(False)
        self.tabWidget.addTab(self.Class1, "")
        self.Class2 = QtWidgets.QWidget()
        self.Class2.setObjectName("Class2")
        self.tabWidget.addTab(self.Class2, "")
        self.Class3 = QtWidgets.QWidget()
        self.Class3.setObjectName("Class3")
        self.tabWidget.addTab(self.Class3, "")
        self.Class4 = QtWidgets.QWidget()
        self.Class4.setObjectName("Class4")
        self.tabWidget.addTab(self.Class4, "")
        self.Class5 = QtWidgets.QWidget()
        self.Class5.setObjectName("Class5")
        self.tabWidget.addTab(self.Class5, "")
        self.Class6 = QtWidgets.QWidget()
        self.Class6.setObjectName("Class6")
        self.tabWidget.addTab(self.Class6, "")
        self.Class7 = QtWidgets.QWidget()
        self.Class7.setObjectName("Class7")
        self.tabWidget.addTab(self.Class7, "")
        self.Class8 = QtWidgets.QWidget()
        self.Class8.setObjectName("Class8")
        self.tabWidget.addTab(self.Class8, "")
        self.treeWidget_2 = QtWidgets.QTreeWidget(Dialog)
        self.treeWidget_2.setGeometry(QtCore.QRect(805, 40, 271, 641))
        self.treeWidget_2.setObjectName("treeWidget_2")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.headerItem().setText(0, _translate("Dialog", "Class / 학수번호 / 교수님 ...."))
        self.treeWidget.headerItem().setText(1, _translate("Dialog", "읽음 표시"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("Dialog", "학습자료실"))
        self.treeWidget.topLevelItem(0).setText(1, _translate("Dialog", "O"))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("Dialog", "자료실_1"))
        self.treeWidget.topLevelItem(0).child(0).setText(1, _translate("Dialog", "O"))
        self.treeWidget.topLevelItem(1).setText(0, _translate("Dialog", "과제"))
        self.treeWidget.topLevelItem(1).setText(1, _translate("Dialog", "O"))
        self.treeWidget.topLevelItem(1).child(0).setText(0, _translate("Dialog", "과제_1"))
        self.treeWidget.topLevelItem(1).child(0).setText(1, _translate("Dialog", "O"))
        self.treeWidget.topLevelItem(2).setText(0, _translate("Dialog", "공지사항"))
        self.treeWidget.topLevelItem(2).setText(1, _translate("Dialog", "X"))
        self.treeWidget.topLevelItem(2).child(0).setText(0, _translate("Dialog", "공지사항_1"))
        self.treeWidget.topLevelItem(2).child(0).setText(1, _translate("Dialog", "X"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Class1), _translate("Dialog", "T_Class1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Class2), _translate("Dialog", "T_Class2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Class3), _translate("Dialog", "T_Class3"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Class4), _translate("Dialog", "T_Class4"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Class5), _translate("Dialog", "T_Class5"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Class6), _translate("Dialog", "T_Class6"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Class7), _translate("Dialog", "T_Class7"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Class8), _translate("Dialog", "T_Class8"))
        self.treeWidget_2.headerItem().setText(0, _translate("Dialog", "과제명"))
        self.treeWidget_2.headerItem().setText(1, _translate("Dialog", "과목명"))
        self.treeWidget_2.headerItem().setText(2, _translate("Dialog", "제출"))
        self.treeWidget_2.headerItem().setText(3, _translate("Dialog", "제출기한"))
        __sortingEnabled = self.treeWidget_2.isSortingEnabled()
        self.treeWidget_2.setSortingEnabled(False)
        self.treeWidget_2.topLevelItem(0).setText(0, _translate("Dialog", "형식언어과제1"))
        self.treeWidget_2.topLevelItem(0).setText(1, _translate("Dialog", "형식언어"))
        self.treeWidget_2.topLevelItem(0).setText(2, _translate("Dialog", "O"))
        self.treeWidget_2.topLevelItem(0).setText(3, _translate("Dialog", "9/10"))
        self.treeWidget_2.topLevelItem(1).setText(0, _translate("Dialog", "자료구조과제1"))
        self.treeWidget_2.topLevelItem(1).setText(1, _translate("Dialog", "자구"))
        self.treeWidget_2.topLevelItem(1).setText(2, _translate("Dialog", "O"))
        self.treeWidget_2.topLevelItem(1).setText(3, _translate("Dialog", "9/11"))
        self.treeWidget_2.topLevelItem(2).setText(0, _translate("Dialog", "자료구조과제2"))
        self.treeWidget_2.topLevelItem(2).setText(1, _translate("Dialog", "자구"))
        self.treeWidget_2.topLevelItem(2).setText(2, _translate("Dialog", "X"))
        self.treeWidget_2.topLevelItem(2).setText(3, _translate("Dialog", "9/12"))
        self.treeWidget_2.setSortingEnabled(__sortingEnabled)


class Action_Main(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
    def CategoryClicked(self):
        print('asdasdasdsa')

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

