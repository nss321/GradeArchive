import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import SignUp
import Main
import User
import sqlite3

form_class = uic.loadUiType("Login.ui")[0]
deny_ui = uic.loadUiType("Deny.ui")[0]
db=sqlite3.connect('./test.db')

#화면을 띄우는데 사용되는 Class 선언
class InitWindow(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.pushButton_signUp.clicked.connect(self.button_signUp)
        self.pushButton_login.clicked.connect(self.button_login)
        self.show()

    def button_signUp(self):
        self.signUp = SignUp.signUpWindow()
        self.signUp.exec_()

    def button_login(self):
        x=list()
        x.append(self.lineEdit_id.text())
        x.append(self.lineEdit_pw.text())
        cnt = 0
        for i in x:
            if i=="":cnt +=1
        
        if cnt == 0:
            try:
                qry='select pw, authority from account where id="'+x[0]+'";'
                cur=db.cursor()
                cur.execute(qry)
                if(cur is not None): 
                    re = cur.fetchall()
                    pw, authority = re[0]
                else: 
                    re.append("")

            except sqlite3.ProgrammingError as e:
                print("error in operation\n")
                print(e)
                db.rollback()
                db.close()
            
            if(x[1]==pw):
                if(authority==0):
                    self.label_5.setText("승인 대기 중인 계정입니다.")
                elif(authority==1):
                    self.callUser(x)
                elif(authority==2):
                    self.callMain()
            else:
                self.label_5.setText("ID 또는 PW를 잘못 입력했습니다.")
                # self.label_5.setText("ID 혹은 PW를 잘못 입력헀습니다.")
        else:
            self.label_5.setText("ID 또는 PW를 입력하지 않았습니다.")

        self.show()
        
    def callMain(self):
        self.hide()
        self.main = Main.mainWindow()
        self.main.exec_()
        self.show()
        self.lineEdit_pw.setText("")
    def callUser(self,x):
        self.hide()
        self.user = User.userWindow(x)
        self.user.exec_()
        self.show()
        self.lineEdit_pw.setText("")


class DenyWindow(QDialog, QWidget, deny_ui):
    def __init__(self):
        super(DenyWindow,self).__init__()
        self.setupUi(self)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = InitWindow()
    myWindow.show()
    app.exec_()