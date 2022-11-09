import sys
from tkinter import X
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sqlite3

edit_ui = uic.loadUiType("EditAccount.ui")[0]
db=sqlite3.connect('./test.db')


collge_list=["인문대학", "사회과학대학", "자연과학대학", "경여대학", "공과대학", "전자정보대학", 
"농업생명환경대학", "사범대학", "생활과학대학", "수의과대학", "약학대학", "의과대학", "자율전공학부", 
"융학학과군"]

department_list=["전기공학부", "전자공학부", "정보통신공학부", "컴퓨터공학과", 
"소프트웨어학부", "지능로봇공학과"]

authority_list=["학생","관리자","승인대기"]


class editWindow(QDialog, QWidget, edit_ui) :
    def __init__(self,x):
        super(editWindow, self).__init__()
        self.initUI(x)
        self.comboBox_1.addItems(collge_list)
        self.comboBox_1.activated[str].connect(lambda :self.selectedComboItem(self.comboBox_1))
        self.comboBox_3.addItems(authority_list)
        self.pushButton_update.clicked.connect(self.updateAccount) #입력된 텍스트 따와서 DB로 쏴야함
        self.pushButton_cancel.clicked.connect(self.Cancel)
        self.show()

    def initUI(self,x):
        self.setupUi(self)
        self.lineEdit_name.setText(x[0])
        self.comboBox_1.addItem(x[3])
        self.comboBox_2.addItem(x[4])
        self.lineEdit_pw.setText(x[2])
        self.lineEdit_id.setText(x[1])
        self.comboBox_3.addItem(x[5])
        self.lineEdit_id.setEnabled(False)
        
    def updateAccount(self):
        row = list()
        row.append(self.lineEdit_name.text()) #name
        row.append(self.comboBox_1.currentText()) #college
        row.append(self.comboBox_2.currentText()) #department
        row.append(self.lineEdit_pw.text()) #pw
        row.append(self.lineEdit_id.text()) #id
        row.append(self.comboBox_3.currentText()) #authority

        if row[5]=="승인대기": row[5]=0
        elif row[5]=="학생": row[5]=1
        elif row[5]=="관리자": row[5]=2
        qry="update account set name=?, pw=?, college=?, department=?, authority=? where id=?;"
        # qry="update account set name=? where id=?;"

        try:
            cur=db.cursor()
            cur.execute(qry, (row[0], row[3], row[1], row[2], row[5], row[4]))
            # cur.execute(qry, (row[0], row[4]))
            db.commit()
            self.close()
        # 디버깅 편의를 위한 에러메시지 출력
        except sqlite3.ProgrammingError as e:
            print("error in operation\n")
            print(e)
            db.rollback()
            db.close()

    def selectedComboItem(self,text): 
        # print(text.currentText()) 
        if text.currentText() == '전자정보대학': 
            self.comboBox_2.clear() 
            self.comboBox_2.addItems(department_list) 

    def Cancel(self):
        self.close()
