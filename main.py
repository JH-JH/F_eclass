import sys
from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtCore import pyqtSlot

class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("Loginform.ui", self)
        self.ui.show()

    @pyqtSlot()
    def LoginClicked(self):
        print(self.ui.userID.text(), self.ui.userPW.text())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Login()
    sys.exit(app.exec())
