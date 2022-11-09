import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

allow_ui = uic.loadUiType("allow.ui")[0]

class allowWindow(QDialog, QWidget, allow_ui) :
    def __init__(self):
        super(allowWindow, self).__init__()
        self.initUI()
        self.pushButton_allow.clicked.connect(self.Cancel)
        self.pushButton_deny.clicked.connect(self.Cancel)
        self.show()

    def initUI(self):
        self.setupUi(self)

    def Cancel(self):
        self.close()
