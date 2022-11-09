import sys
from tkinter import X
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sqlite3

edit_ui = uic.loadUiType("Input.ui")[0]
db=sqlite3.connect('./test.db')


year=["-", "2017", "2018", "2019", "2020", "2021", "2022"]

semester=["-", "1학기", "2학기", "여름학기", "겨울학기"]

category=["-", "교양선택", "교양필수", "전공선택", "전공필수", "일반선택"]


class editWindow(QDialog, QWidget, edit_ui) :
    # data = list("1")
    def __init__(self,x):
        super(editWindow, self).__init__()
        self.initUI(x)
        # self.data = list("1")
        self.pushButton_input.clicked.connect(self.updateData) #입력된 텍스트 따와서 DB로 쏴야함
        self.pushButton_cancel.clicked.connect(self.Cancel)
        self.pushButton_isvalid.clicked.connect(self.isValid)
        self.show()

    def initUI(self,x):
        self.setupUi(self)
        self.lineEdit_name.setText(x[0])
        self.comboBox_year.addItem(x[1])
        self.comboBox_semester.addItem(x[2])
        self.comboBox_category.addItem(x[4])
        self.lineEdit_subject.setText(x[3])
        self.lineEdit_name.setEnabled(False)
        self.comboBox_year.setEnabled(False)
        self.comboBox_semester.setEnabled(False)
        self.comboBox_category.setEnabled(False)
        self.lineEdit_subject.setEnabled(False)
        


    def updateData(self):
        row = list()
        row.append(self.lineEdit_name.text())
        row.append(self.comboBox_year.currentText())
        row.append(self.comboBox_semester.currentText())
        row.append(self.comboBox_category.currentText())
        row.append(self.lineEdit_subject.text())
        row.append(self.lineEdit_credit.text())
        row.append(self.lineEdit_grade.text())
        row.append(self.lineEdit_validate.text())
        
        if(row[-1]=="" and row[-1]=="빈칸이 있습니다."):
            self.lineEdit_validate.setStyleSheet("background : red; color : white;")
            self.lineEdit_validate.text("유효성 검사를 해주세요.")
        else:
            qry="update data set credit=?, grade=? where name=? and year=? and semester=? and subject=?;"
            try:
                cur=db.cursor()
                cur.execute(qry, (row[5], row[6], row[0], row[1], row[2], row[4]))
                db.commit()
                self.close()
            # 디버깅 편의를 위한 에러메시지 출력
            except sqlite3.ProgrammingError as e:
                print("error in operation\n")
                print(e)
                db.rollback()
                db.close()

    def isValid(self):
        row = list()
        cnt = 0
        row.append(self.lineEdit_name.text())
        row.append(self.comboBox_year.currentText())
        row.append(self.comboBox_semester.currentText())
        row.append(self.comboBox_category.currentText())
        row.append(self.lineEdit_subject.text())
        row.append(self.lineEdit_credit.text())
        row.append(self.lineEdit_grade.text())
        
        qry = 'SELECT id from account where name = "' +row[0]+ '";'
        try:
            cur = db.cursor()
            cur.execute(qry)
            tmp_id = cur.fetchone()
            # self.lineEdit_validate.setText(str(type(tmp_id)))

        except sqlite3.ProgrammingError as e:
            print("error in operation\n")
            print(e)
            db.rollback()
            db.close()
        # self.lineEdit_subject.setText(row[4])
        
        for x in row:
            if(x == ""):
                cnt += 1
        if(cnt == 0):
            if(tmp_id is not None):
                self.lineEdit_validate.setStyleSheet("background : green; color : black;")
                self.lineEdit_validate.setText(tmp_id[0])
            else:
                self.lineEdit_validate.setStyleSheet("background : pink; color : black;")
                self.lineEdit_validate.setText("존재하지 않는 학생입니다.")
        else:
            self.lineEdit_validate.setStyleSheet("background : pink; color : black;")
            self.lineEdit_validate.setText("빈칸이 있습니다.")

    def Cancel(self):
        self.close()
