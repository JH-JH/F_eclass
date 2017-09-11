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

    def treeWidgetItemInit(self, i):
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgets[i])
        item_0.setExpanded(True)
        if len(self.classContent[i]) > 0:
            for num in range(self.classContent[i][0]):
                QtWidgets.QTreeWidgetItem(item_0)

        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgets[i])
        item_0.setExpanded(True)
        if len(self.classContent[i]) > 1:
            for num in range(self.classContent[i][1]):
                QtWidgets.QTreeWidgetItem(item_0)

        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgets[i])
        item_0.setExpanded(True)
        if len(self.classContent[i]) > 2:
            for num in range(self.classContent[i][2]):
                QtWidgets.QTreeWidgetItem(item_0)

        self.treeWidgets[i].header().setCascadingSectionResizes(True)
        self.treeWidgets[i].header().resizeSection(0, 400)
        self.treeWidgets[i].header().setMinimumSectionSize(300)
        self.treeWidgets[i].header().setHighlightSections(True)
        self.treeWidgets[i].header().setSortIndicatorShown(False)


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

    '''
    def treeWidgetItemInit(self, class_idx ,content_num ):
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgets[class_idx])
        item_0.setExpanded(True)
        QtWidgets.QTreeWidgetItem(item_0)
    '''

    def setupUi(self, Dialog):
        print(-1)
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(1086, 819)
        Dialog.setAutoFillBackground(False)
        print(0)

        self.tabWidgetInit()
        self.addtabInit()
        print(1)

        # <treeWidget/ WidgetItem Init>
        self.treeWidgets = []
        for i in range(self.class_num):
            self.treeWidgets.append(QtWidgets.QTreeWidget(self.Classes[i]))
            print('2_1')
            self.treeWidgetInit(self.treeWidgets[i])
            print('2_2')
            self.treeWidgetItemInit(i)
            print('2_3')
        # </treeWidget/ WidgetItem Init>
        print(2)

        #item setup
        self._translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle( self._translate("Dialog", "E-Class"))

        #set tabName & class Widget Init
        for i in range(self.class_num):
            self.setTabWidgetName(i,"class"+str(i))
            __sortingEnabled = self.treeWidgets[i].isSortingEnabled()
            self.treeWidgets[i].setSortingEnabled(__sortingEnabled)
            self.treeWidgets[i].headerItem().setText(0,  self._translate("Dialog", "Class / 학수번호 / 교수님 ...."))
            self.treeWidgets[i].headerItem().setText(1,  self._translate("Dialog", "읽음 표시"))
        print(3)

        #<tree2>
        self.treeWidgetInit2()
        self.treeWidgetItemInit2()
        self.tree2Init()
        #</tree2>

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def setCategory(self, Class_ix, row, categoryName, ischecked):
        self.treeWidgets[Class_ix].topLevelItem(row).setText(0, self._translate("Dialog", categoryName))
        self.treeWidgets[Class_ix].topLevelItem(row).setText(1, self._translate("Dialog", ischecked))

    def setContent(self, Class_ix, row, sub_row, contentName, ischecked):
        self.treeWidgets[Class_ix].topLevelItem(row).child(sub_row).setText(0,  self._translate("Dialog", contentName))
        self.treeWidgets[Class_ix].topLevelItem(row).child(sub_row).setText(1,  self._translate("Dialog", ischecked))

    def tree2Init(self):
        # 트리2 초기 구문
        self.treeWidget_2.headerItem().setText(0,  self._translate("Dialog", "과제명"))
        self.treeWidget_2.headerItem().setText(1,  self._translate("Dialog", "과목명"))
        self.treeWidget_2.headerItem().setText(2,  self._translate("Dialog", "제출"))
        self.treeWidget_2.headerItem().setText(3,  self._translate("Dialog", "제출기한"))
        __sortingEnabled = self.treeWidget_2.isSortingEnabled()
        self.treeWidget_2.setSortingEnabled(False)

    def tree2Item(self,row,content,className, checked, d_day):
        # 트리 내용
        self.treeWidget_2.topLevelItem(row).setText(0,  self._translate("Dialog", content))
        self.treeWidget_2.topLevelItem(row).setText(1,  self._translate("Dialog", className))
        self.treeWidget_2.topLevelItem(row).setText(2,  self._translate("Dialog", checked))
        self.treeWidget_2.topLevelItem(row).setText(3,  self._translate("Dialog", d_day))
        __sortingEnabled = self.treeWidget_2.isSortingEnabled()
        self.treeWidget_2.setSortingEnabled(__sortingEnabled)
    def Init(self,class_num):
        self.classContent = []
        self.class_num = class_num
        for i in range(self.class_num):
            self.classContent.append([])

    def setContentNum(self, class_idx, col_num):
        self.classContent[class_idx].append(col_num)




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

    #<login>
    Dialog = Action_Login()
    Dialog.ui = Ui_Login()
    Dialog.ui.setupUi(Dialog)
    Dialog.show()
    app.exec_()  # for LoginDialog
    #</login>


    Dialog = Action_Main()
    Dialog.ui = Ui_Main()
    class_num = 5
    Dialog.ui.Init(class_num)
    # (class_ix, col_num)
    Dialog.ui.setContentNum(0, 2)
    Dialog.ui.setContentNum(0, 1)
    Dialog.ui.setContentNum(0, 1)
    Dialog.ui.setContentNum(1, 1)
    Dialog.ui.setContentNum(1, 1)
    Dialog.ui.setContentNum(1, 1)

    print('ui start')
    Dialog.ui.setupUi(Dialog)
    Dialog.show()
    ##Task Itme
    class_ix = 0
    Dialog.ui.setTabWidgetName(class_ix, "형식언어")
    # <set Item(class_idx, row_num, subrow_num,"name", ischecked)>
    Dialog.ui.setCategory(class_ix, 0, "학습자료실", "O")
    Dialog.ui.setContent(class_ix,0,0,"자료실_1","O")
    Dialog.ui.setContent(class_ix, 0, 1, "자료실_2", "O")

    Dialog.ui.setCategory(class_ix, 1, "과제", "O")
    Dialog.ui.setContent(class_ix, 1, 0, "과제_1", "O")

    Dialog.ui.setCategory(class_ix, 2, "공지사항", "X")
    Dialog.ui.setContent(class_ix, 2, 0, "공지사항_1", "X")
    # </set Item(class_idx, row_num, subrow_num,"name", ischecked)>
    ###

    ##Task Itme
    class_ix = 1
    Dialog.ui.setTabWidgetName(class_ix, "자료구조")
    # <set Item(class_idx, row_num, subrow_num,"name", ischecked)>
    Dialog.ui.setCategory(class_ix, 0, "학습자료실", "O")
    Dialog.ui.setContent(class_ix, 0, 0, "자료구조실_1", "O")

    Dialog.ui.setCategory(class_ix, 1, "과제", "O")
    Dialog.ui.setContent(class_ix, 1, 0, "과제란망할놈_1", "O")

    Dialog.ui.setCategory(class_ix, 2, "공지사항", "X")
    Dialog.ui.setContent(class_ix, 2, 0, "공지사항서양_1", "X")
    # </set Item(class_idx, row_num, subrow_num,"name", ischecked)>
    ###

    # <tree2Content>
    Dialog.ui.tree2Item(0, "형식언어과제1", "형식언어", "O", "9/10")
    Dialog.ui.tree2Item(1, "자료구조과제1", "자구", "O", "9/11")
    Dialog.ui.tree2Item(2, "자료구조과제2", "자구", "X", "9/12")
    # </tree2Content>

    app.exec_()  # for MainDialog

