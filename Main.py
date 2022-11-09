import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import Input
import Account
import Editdata
import sqlite3

main_ui = uic.loadUiType("Main.ui")[0]
db=sqlite3.connect('./test.db')


class mainWindow(QDialog, QWidget, main_ui) :
    def __init__(self):
        super(mainWindow, self).__init__()
        self.initUI()
        self.drawTable()
        self.pushButton_logout.clicked.connect(self.Cancel)
        self.pushButton_search.clicked.connect(self.button_search)
        self.pushButton_input.clicked.connect(self.button_input)
        self.pushButton_edit.clicked.connect(self.button_edit)
        self.pushButton_delete.clicked.connect(self.button_delete)
        # self.pushButton_upload.clicked.connect(self.button_upload)
        # self.pushButton_download.clicked.connect(self.button_download)
        self.pushButton_account.clicked.connect(self.button_account)
        self.pushButton_refresh.clicked.connect(self.drawTable)
        self.show()

    def initUI(self):
        self.setupUi(self)


    def drawTable(self):
        qry="SELECT * from data;"
        cur=db.cursor()
        cur.execute(qry) 
        rows = cur.fetchall()
        count = len(rows)

        self.tableWidget.setRowCount(count)
        
        for x in range(count):
        #리스트 내부의 column쌍은 튜플로 반환하므로 튜플의 각 값을 변수에 저장
            name, year, semester, subject, category, credit, grade, id = rows[x]
            
            #테이블의 각 셀에 값 입력
            self.tableWidget.setItem(x, 0, QTableWidgetItem(name))
            self.tableWidget.setItem(x, 1, QTableWidgetItem(year))
            self.tableWidget.setItem(x, 2, QTableWidgetItem(semester))
            self.tableWidget.setItem(x, 3, QTableWidgetItem(subject))   
            self.tableWidget.setItem(x, 4, QTableWidgetItem(category))
            self.tableWidget.setItem(x, 5, QTableWidgetItem(str(credit)))
            self.tableWidget.setItem(x, 6, QTableWidgetItem(grade))
            self.tableWidget.setItem(x, 7, QTableWidgetItem(str(id))) 
        self.tableWidget.setSortingEnabled(True)


    def button_input(self):
        self.input = Input.inputWindow()
        self.input.exec_()
        
    def button_edit(self):
        target = self.tableWidget.selectedIndexes()
        x = list()
        x.append(self.tableWidget.item(target[0].row(), 0).text()) #name
        x.append(self.tableWidget.item(target[0].row(), 1).text()) #year
        x.append(self.tableWidget.item(target[0].row(), 2).text()) #semester
        x.append(self.tableWidget.item(target[0].row(), 3).text()) #subject
        x.append(self.tableWidget.item(target[0].row(), 4).text()) #category
        x.append(self.tableWidget.item(target[0].row(), 5).text()) #credit
        x.append(self.tableWidget.item(target[0].row(), 6).text()) #grade
        
        self.edit = Editdata.editWindow(x)
        # self.edit.setData(x)
        self.edit.exec_()
        # self.edit.setData(x)


    # def button_upload(self):
    
    # def button_download(self):

    def button_search(self):
        if(self.radioButton_id.isChecked()):
            keyword = self.lineEdit_search.text()
            qry='SELECT * from data where id == "'+keyword+'";'
            cur=db.cursor()
            cur.execute(qry) 
            rows = cur.fetchall()
            count = len(rows)
            cur.close()

            self.tableWidget.setRowCount(count)
            
            for x in range(count):
            #리스트 내부의 column쌍은 튜플로 반환하므로 튜플의 각 값을 변수에 저장
                name, year, semester, subject, category, credit, grade, id = rows[x]
                
                #테이블의 각 셀에 값 입력
                self.tableWidget.setItem(x, 0, QTableWidgetItem(name))
                self.tableWidget.setItem(x, 1, QTableWidgetItem(year))
                self.tableWidget.setItem(x, 2, QTableWidgetItem(semester))
                self.tableWidget.setItem(x, 3, QTableWidgetItem(subject))   
                self.tableWidget.setItem(x, 4, QTableWidgetItem(category))
                self.tableWidget.setItem(x, 5, QTableWidgetItem(str(credit)))
                self.tableWidget.setItem(x, 6, QTableWidgetItem(grade))
                self.tableWidget.setItem(x, 7, QTableWidgetItem(str(id))) 
        
        elif(self.radioButton_name.isChecked()):
            keyword = self.lineEdit_search.text()
            qry='SELECT * from data where name == "'+keyword+'";'
            cur=db.cursor()
            cur.execute(qry) 
            rows = cur.fetchall()
            count = len(rows)
            cur.close()

            self.tableWidget.setRowCount(count)
            
            for x in range(count):
            #리스트 내부의 column쌍은 튜플로 반환하므로 튜플의 각 값을 변수에 저장
                name, year, semester, subject, category, credit, grade, id = rows[x]
                
                #테이블의 각 셀에 값 입력
                self.tableWidget.setItem(x, 0, QTableWidgetItem(name))
                self.tableWidget.setItem(x, 1, QTableWidgetItem(year))
                self.tableWidget.setItem(x, 2, QTableWidgetItem(semester))
                self.tableWidget.setItem(x, 3, QTableWidgetItem(subject))   
                self.tableWidget.setItem(x, 4, QTableWidgetItem(category))
                self.tableWidget.setItem(x, 5, QTableWidgetItem(str(credit)))
                self.tableWidget.setItem(x, 6, QTableWidgetItem(grade))
                self.tableWidget.setItem(x, 7, QTableWidgetItem(str(id))) 
        
    def button_account(self):
        self.account = Account.accountWindow()
        self.account.exec_()

    def button_delete(self):
        target = self.tableWidget.selectedIndexes()
        keyword = self.tableWidget.item(target[0].row(), target[0].column()).text()
        x = list()
        x.append(self.tableWidget.item(target[0].row(), 0).text()) #name
        x.append(self.tableWidget.item(target[0].row(), 1).text()) #year
        x.append(self.tableWidget.item(target[0].row(), 2).text()) #semester
        x.append(self.tableWidget.item(target[0].row(), 3).text()) #subject
        
        # self.lineEdit_search.setText(keyword)
        
        if(x):
            try:
                qry='DELETE from data where name == "' + x[0] + '" AND year == "' + x[1] + '" AND semester == "' + x[2] + '" AND subject == "' + x[3] + '";'                          
                # qry="delete from data where name=? and year=? and semester=? and subject=? and id=?;"
                # qry='SELECT * from data where name == "' + x[0] + '" AND year == "' + x[1] + '" AND semester == "' + x[2] + '" AND subject == "' + x[3] + '";'                          
                cur=db.cursor()
                cur.execute(qry) 
                db.commit()
                self.drawTable()

            except sqlite3.ProgrammingError as e:
                print("error in operation\n")
                print(e)
                db.rollback
                db.close()


        # self.lineEdit_search.setText(rows[0]+rows[3])
    
    def Cancel(self):
        db.close()
        self.close()

