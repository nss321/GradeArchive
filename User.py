import sys
from turtle import xcor
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sqlite3

user_ui = uic.loadUiType("User.ui")[0]
db=sqlite3.connect('./test.db')

semester=["-", "1학기", "2학기", "여름학기", "겨울학기"]

class userWindow(QDialog, QWidget, user_ui) :
    def __init__(self,x):
        super(userWindow, self).__init__()
        self.initUI()
        self.info = x
        self.drawTable()
        self.pushButton_logout.clicked.connect(self.Cancel)
        # self.pushButton_download.clicked.connect(self.button_download)
        self.comboBox.activated[str].connect(lambda :self.selectedComboItem(self.info, self.comboBox))
        self.pushButton_refresh.clicked.connect(self.drawTable)
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.comboBox.addItems(semester)


    def drawTable(self):
        qry='SELECT * from data where id="'+self.info[0]+'";'
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

    # def drawTable(self,x):
    #     qry='SELECT * from data where id="'+x[0]+'";'
    #     cur=db.cursor()
    #     cur.execute(qry) 
    #     rows = cur.fetchall()
    #     count = len(rows)

    #     self.tableWidget.setRowCount(count)
        
    #     for x in range(count):
    #     #리스트 내부의 column쌍은 튜플로 반환하므로 튜플의 각 값을 변수에 저장
    #         name, year, semester, subject, category, credit, grade, id = rows[x]
            
    #         #테이블의 각 셀에 값 입력
    #         self.tableWidget.setItem(x, 0, QTableWidgetItem(name))
    #         self.tableWidget.setItem(x, 1, QTableWidgetItem(year))
    #         self.tableWidget.setItem(x, 2, QTableWidgetItem(semester))
    #         self.tableWidget.setItem(x, 3, QTableWidgetItem(subject))   
    #         self.tableWidget.setItem(x, 4, QTableWidgetItem(category))
    #         self.tableWidget.setItem(x, 5, QTableWidgetItem(str(credit)))
    #         self.tableWidget.setItem(x, 6, QTableWidgetItem(grade))
    #         self.tableWidget.setItem(x, 7, QTableWidgetItem(str(id))) 
    #     self.tableWidget.setSortingEnabled(True)
    
    def filterTable(self,x,text):
        qry='SELECT * from data where id="'+x[0]+'" and semester="'+text+'";'
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


    def selectedComboItem(self,x,text): 
        # print(text.currentText()) 
        if text.currentText() == "1학기": 
            self.filterTable(x, text.currentText())
        elif text.currentText() == "2학기": 
            self.filterTable(x, text.currentText())
        elif text.currentText() == "여름학기": 
                    self.filterTable(x, text.currentText())
        elif text.currentText() == "겨울학기": 
                    self.filterTable(x, text.currentText())


    def Cancel(self):
        db.close()
        self.close()


