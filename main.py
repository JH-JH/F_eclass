# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
#import core


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
    def tabWidgetInit(self):
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 781, 681))
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")

    def addtabInit(self):
        self.Classes = []
        for i in range(self.class_num):
            print(i)
            self.Classes.insert(0,QtWidgets.QWidget())

        for i in range(self.class_num):
            self.Classes[i].setObjectName("Class"+str(i))
            self.tabWidget.addTab(self.Classes[i], "")

    def treeWidgetInit(self, treeWidget):
        treeWidget.setGeometry(QtCore.QRect(10, 10, 761, 641))
        font = QtGui.QFont()
        font.setPointSize(10)
        treeWidget.setFont(font)
        treeWidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        treeWidget.setAcceptDrops(False)
        treeWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        treeWidget.setAutoFillBackground(False)
        treeWidget.setInputMethodHints(QtCore.Qt.ImhNone)
        treeWidget.setAnimated(False)
        treeWidget.setAllColumnsShowFocus(False)
        treeWidget.setHeaderHidden(False)
        treeWidget.setObjectName("treeWidget")

    def treeWidgetItemInit(self, treeWidget):
        item_0 = QtWidgets.QTreeWidgetItem(treeWidget)
        item_0.setExpanded(True)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)

        item_0 = QtWidgets.QTreeWidgetItem(treeWidget)
        item_0.setExpanded(True)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)

        item_0 = QtWidgets.QTreeWidgetItem(treeWidget)
        item_0.setExpanded(True)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)

        self.treeWidgets[0].header().setCascadingSectionResizes(True)
        self.treeWidgets[0].header().resizeSection(0, 400)
        self.treeWidgets[0].header().setMinimumSectionSize(300)
        self.treeWidgets[0].header().setHighlightSections(True)
        self.treeWidgets[0].header().setSortIndicatorShown(False)

    def treeWidgetInit2(self):
        self.treeWidget_2 = QtWidgets.QTreeWidget(Dialog)
        self.treeWidget_2.setGeometry(QtCore.QRect(805, 40, 271, 641))
        self.treeWidget_2.setObjectName("treeWidget_2")
    def treeWidgetItemInit2(self):
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_2)

    def setTabWidgetName(self,class_ix, class_name):
        # 탭 이름 설정#
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Classes[class_ix]),  self._translate("Dialog", class_name))

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(1086, 819)
        Dialog.setAutoFillBackground(False)
        self.class_num = 8

        self.tabWidgetInit()
        self.addtabInit()

        # <treeWidget/ WidgetItem Init>
        self.treeWidgets = [QtWidgets.QTreeWidget(self.Classes[0]), QtWidgets.QTreeWidget(self.Classes[1]),
                            QtWidgets.QTreeWidget(self.Classes[2]),
                            QtWidgets.QTreeWidget(self.Classes[3]), QtWidgets.QTreeWidget(self.Classes[4]),
                            QtWidgets.QTreeWidget(self.Classes[5]),
                            QtWidgets.QTreeWidget(self.Classes[6]), QtWidgets.QTreeWidget(self.Classes[7])]

        for i in range(self.class_num):
            self.treeWidgetInit(self.treeWidgets[i])
            self.treeWidgetItemInit(self.treeWidgets[i])
        # </treeWidget/ WidgetItem Init>

        #item setup
        self._translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle( self._translate("Dialog", "Dialog"))

        #set tabName & class Widget Init
        for i in range(self.class_num):
            self.setTabWidgetName(i,"class"+str(i))
            __sortingEnabled = self.treeWidgets[i].isSortingEnabled()
            self.treeWidgets[i].setSortingEnabled(__sortingEnabled)

        ##Task Itme
        class_ix = 0
        self.setTabWidgetName(class_ix, "형식언어")
        #set ItemHeader (class_idx, col_num)
        self.treeWidgets[class_ix].headerItem().setText(0,  self._translate("Dialog", "Class / 학수번호 / 교수님 ...."))
        self.treeWidgets[class_ix].headerItem().setText(1,  self._translate("Dialog", "읽음 표시"))
        # <set Item(class_idx, row_num, subrow_num,"name", ischecked)>
        self.setCategory(class_ix,0,"학습자료실","O")
        self.setContent(class_ix,0,0,"자료실_1","O")

        self.setCategory(class_ix, 1, "과제", "O")
        self.setContent(class_ix,1,0,"과제_1","O")

        self.setCategory(class_ix, 2, "공지사항", "X")
        self.setContent(class_ix,2,0,"공지사항_1","X")
        # </set Item(class_idx, row_num, subrow_num,"name", ischecked)>
        ###

        ##Task Itme
        class_ix = 1
        self.setTabWidgetName(class_ix, "자료구조")
        #set ItemHeader (class_idx, col_num)
        self.treeWidgets[class_ix].headerItem().setText(0,  self._translate("Dialog", "Class / 학수번호 / 교수님 ...."))
        self.treeWidgets[class_ix].headerItem().setText(1,  self._translate("Dialog", "읽음 표시"))
        # <set Item(class_idx, row_num, subrow_num,"name", ischecked)>
        self.setCategory(class_ix,0,"학습자료실","O")
        self.setContent(class_ix,0,0,"자료구조실_1","O")

        self.setCategory(class_ix, 1, "과제", "O")
        self.setContent(class_ix,1,0,"과제란망할놈_1","O")

        self.setCategory(class_ix, 2, "공지사항", "X")
        self.setContent(class_ix,2,0,"공지사항서양_1","X")
        # </set Item(class_idx, row_num, subrow_num,"name", ischecked)>
        ###

        #<tree2>
        self.treeWidgetInit2()
        self.treeWidgetItemInit2()
        self.tree2()
        #</tree2>

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)




    def setCategory(self, Class_ix, row, categoryName, ischecked):
        self.treeWidgets[Class_ix].topLevelItem(row).setText(0, self._translate("Dialog", categoryName))
        self.treeWidgets[Class_ix].topLevelItem(row).setText(1, self._translate("Dialog", ischecked))

    def setContent(self, Class_ix, row, sub_row, contentName, ischecked):
        self.treeWidgets[Class_ix].topLevelItem(row).child(sub_row).setText(0,  self._translate("Dialog", contentName))
        self.treeWidgets[Class_ix].topLevelItem(row).child(sub_row).setText(1,  self._translate("Dialog", ischecked))

    def tree2(self):
        # 트리2 초기 구문
        self.treeWidget_2.headerItem().setText(0,  self._translate("Dialog", "과제명"))
        self.treeWidget_2.headerItem().setText(1,  self._translate("Dialog", "과목명"))
        self.treeWidget_2.headerItem().setText(2,  self._translate("Dialog", "제출"))
        self.treeWidget_2.headerItem().setText(3,  self._translate("Dialog", "제출기한"))
        __sortingEnabled = self.treeWidget_2.isSortingEnabled()
        self.treeWidget_2.setSortingEnabled(False)

        # 트리 내용
        self.treeWidget_2.topLevelItem(0).setText(0,  self._translate("Dialog", "형식언어과제1"))
        self.treeWidget_2.topLevelItem(0).setText(1,  self._translate("Dialog", "형식언어"))
        self.treeWidget_2.topLevelItem(0).setText(2,  self._translate("Dialog", "O"))
        self.treeWidget_2.topLevelItem(0).setText(3,  self._translate("Dialog", "9/10"))
        self.treeWidget_2.topLevelItem(1).setText(0,  self._translate("Dialog", "자료구조과제1"))
        self.treeWidget_2.topLevelItem(1).setText(1,  self._translate("Dialog", "자구"))
        self.treeWidget_2.topLevelItem(1).setText(2,  self._translate("Dialog", "O"))
        self.treeWidget_2.topLevelItem(1).setText(3,  self._translate("Dialog", "9/11"))
        self.treeWidget_2.topLevelItem(2).setText(0,  self._translate("Dialog", "자료구조과제2"))
        self.treeWidget_2.topLevelItem(2).setText(1,  self._translate("Dialog", "자구"))
        self.treeWidget_2.topLevelItem(2).setText(2,  self._translate("Dialog", "X"))
        self.treeWidget_2.topLevelItem(2).setText(3,  self._translate("Dialog", "9/12"))
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
    app.exec_()  # for LoginDialog
    app.exec_()  # for MainDialog

