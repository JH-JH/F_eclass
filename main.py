import sys
from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtCore import pyqtSlot

id = ""
pw = ""
class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("Loginform.ui", self)
        self.ui.show()

    @pyqtSlot()
    def LoginClicked(self):
        global id, pw
        id = self.ui.userID.text()
        pw = self.ui.userPW.text()
        print(id,pw)

app = QtWidgets.QApplication(sys.argv)
w = Login()
sys.exit(app.exec())