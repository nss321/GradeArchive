import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import Allow
import EditAccount
import sqlite3

account_ui = uic.loadUiType("account.ui")[0]
db=sqlite3.connect('./test.db')

class accountWindow(QDialog, QWidget, account_ui) :
    def __init__(self):
        super(accountWindow, self).__init__()
        self.initUI()
        # self.pushButton_allow.clicked.connect(self.button_allow)
        self.pushButton_edit.clicked.connect(self.button_edit)
        self.pushButton_delete.clicked.connect(self.button_delete)
        self.pushButton_search.clicked.connect(self.button_search)
        self.pushButton_cancel.clicked.connect(self.Cancel)
        self.pushButton_refresh.clicked.connect(self.drawTable)
        self.drawTable()
        self.show()

    def initUI(self):
        self.setupUi(self)

    def drawTable(self):
        qry="select * from account;"
        cur=db.cursor()
        cur.execute(qry) 
        rows = cur.fetchall()
        count = len(rows)

        self.tableWidget.setRowCount(count)
        
        for x in range(count):
        #리스트 내부의 column쌍은 튜플로 반환하므로 튜플의 각 값을 변수에 저장
            name, id, pw, college, department, authority = rows[x]
            if authority==0: authority="승인대기"
            elif authority==1: authority="학생"
            elif authority==2: authority="관리자"

            #테이블의 각 셀에 값 입력
            self.tableWidget.setItem(x, 0, QTableWidgetItem(name))
            self.tableWidget.setItem(x, 1, QTableWidgetItem(id))
            self.tableWidget.setItem(x, 2, QTableWidgetItem(pw))
            self.tableWidget.setItem(x, 3, QTableWidgetItem(college))   
            self.tableWidget.setItem(x, 4, QTableWidgetItem(department))
            self.tableWidget.setItem(x, 5, QTableWidgetItem(str(authority)))
        self.tableWidget.setSortingEnabled(True)


    def button_allow(self):
        self.signUp = Allow.allowWindow()
        self.signUp.exec_()

    def button_edit(self):
            target = self.tableWidget.selectedIndexes()
            x = list()
            x.append(self.tableWidget.item(target[0].row(), 0).text()) #name
            x.append(self.tableWidget.item(target[0].row(), 1).text()) #id
            x.append(self.tableWidget.item(target[0].row(), 2).text()) #pw
            x.append(self.tableWidget.item(target[0].row(), 3).text()) #college
            x.append(self.tableWidget.item(target[0].row(), 4).text()) #department
            x.append(self.tableWidget.item(target[0].row(), 5).text()) #authority
            
            self.edit = EditAccount.editWindow(x)
            self.edit.exec_()
    

    def button_search(self):
        if(self.radioButton_id.isChecked()):
            keyword = self.lineEdit_search.text()
            qry='SELECT * from account where id == "'+keyword+'";'
            cur=db.cursor()
            cur.execute(qry) 
            rows = cur.fetchall()
            count = len(rows)

            self.tableWidget.setRowCount(count)
            
            for x in range(count):
            #리스트 내부의 column쌍은 튜플로 반환하므로 튜플의 각 값을 변수에 저장
                name, id, pw, college, department, authority = rows[x]
                if authority==0: authority="승인대기"
                elif authority==1: authority="학생"
                elif authority==2: authority="관리자"
                
                #테이블의 각 셀에 값 입력
                self.tableWidget.setItem(x, 0, QTableWidgetItem(name))
                self.tableWidget.setItem(x, 1, QTableWidgetItem(id))
                self.tableWidget.setItem(x, 2, QTableWidgetItem(pw))
                self.tableWidget.setItem(x, 3, QTableWidgetItem(college))   
                self.tableWidget.setItem(x, 4, QTableWidgetItem(department))
                self.tableWidget.setItem(x, 5, QTableWidgetItem(str(authority)))
            self.tableWidget.setSortingEnabled(True)


        elif(self.radioButton_name.isChecked()):
            keyword = self.lineEdit_search.text()
            qry='SELECT * from account where name == "'+keyword+'";'
            cur=db.cursor()
            cur.execute(qry) 
            rows = cur.fetchall()
            count = len(rows)

            self.tableWidget.setRowCount(count)
            
            for x in range(count):
            #리스트 내부의 column쌍은 튜플로 반환하므로 튜플의 각 값을 변수에 저장
                name, id, pw, college, department, authority = rows[x]
                if authority==0: authority="승인대기"
                elif authority==1: authority="학생"
                elif authority==2: authority="관리자"
                
                #테이블의 각 셀에 값 입력
                self.tableWidget.setItem(x, 0, QTableWidgetItem(name))
                self.tableWidget.setItem(x, 1, QTableWidgetItem(id))
                self.tableWidget.setItem(x, 2, QTableWidgetItem(pw))
                self.tableWidget.setItem(x, 3, QTableWidgetItem(college))   
                self.tableWidget.setItem(x, 4, QTableWidgetItem(department))
                self.tableWidget.setItem(x, 5, QTableWidgetItem(str(authority)))
            self.tableWidget.setSortingEnabled(True) 
        
    def button_delete(self):
        target = self.tableWidget.selectedIndexes()
        keyword = self.tableWidget.item(target[0].row(), 1).text()
        try:
            qry='DELETE from account where id="'+keyword+'";'                          
            cur=db.cursor()
            cur.execute(qry) 
            db.commit()
            self.drawTable()

        except sqlite3.ProgrammingError as e:
            print("error in operation\n")
            print(e)
            db.rollback
            db.close()
        # self.lineEdit_search.setText(keyword)

    def Cancel(self):
        self.close()
