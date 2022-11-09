import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sqlite3

signup_ui = uic.loadUiType("SignUp.ui")[0]
db=sqlite3.connect('./test.db')


collge_list=["인문대학", "사회과학대학", "자연과학대학", "경여대학", "공과대학", "전자정보대학", 
"농업생명환경대학", "사범대학", "생활과학대학", "수의과대학", "약학대학", "의과대학", "자율전공학부", 
"융학학과군"]

department_list=["전기공학부", "전자공학부", "정보통신공학부", "컴퓨터공학과", 
"소프트웨어학부", "지능로봇공학과"]


class signUpWindow(QDialog, QWidget, signup_ui) :
    def __init__(self):
        super(signUpWindow, self).__init__()
        self.initUI()
        self.comboBox_1.addItems(collge_list)
        self.comboBox_1.activated[str].connect(lambda :self.selectedComboItem(self.comboBox_1))
        self.comboBox_2.addItem("-")
        self.pushButton_1.clicked.connect(self.button_signUp)
        self.pushButton_2.clicked.connect(self.Cancel)
        self.show()

    def initUI(self):
        self.setupUi(self)

    def selectedComboItem(self,text): 
        # print(text.currentText()) 
        if text.currentText() == '전자정보대학': 
            self.comboBox_2.clear() 
            self.comboBox_2.addItems(department_list) 
            
    def button_signUp(self):
        row = list()
        row.append(self.lineEdit_name.text())
        row.append(self.comboBox_1.currentText())
        row.append(self.comboBox_2.currentText())
        row.append(self.lineEdit_pw.text())
        row.append(self.lineEdit_id.text())

        cnt = 0
        for x in row:
            if x == "": cnt += 1

        if cnt == 0:
            qry="insert into account (name, id, pw, college, department, authority) values(?,?,?,?,?,?);"
            try:
                cur=db.cursor()
                cur.execute(qry, (row[0], row[4], row[3], row[1], row[2], 0))
                db.commit()
                db.close()
                self.close()
            # 디버깅 편의를 위한 에러메시지 출력
            except sqlite3.ProgrammingError as e:
                print("error in operation\n")
                print(e)
                db.rollback()
                db.close()

    def Cancel(self):
        self.close()
