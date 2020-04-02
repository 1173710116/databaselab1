import pymysql
from PyQt5.Qt import QWidget
from PyQt5 import QtGui,QtWidgets
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import (QFrame, QApplication, QDialog, QDialogButtonBox, QHeaderView, QLabel,
        QMessageBox, QVBoxLayout, QLineEdit, QTableWidgetItem, QTableWidget, QHBoxLayout, QPushButton)
from functools import partial
import sys
import datetime


class MainPage(QDialog):
    def __init__(self, username, parent=None):
        super(MainPage, self).__init__(parent)

        self.username = username
        self.resize(800, 800)
        self.setWindowTitle('博客')
        self.setWindowFlags(Qt.Widget)

        connection = pymysql.connect(host='localhost', port=3306, user='root',
                                     password='000000', db='database_lab1', charset='utf8')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM blogs")
        data = cursor.fetchall()
        print(data)

        col_lst = [tup[0] for tup in cursor.description]

        row = len(data)
        vol = len(data[0])

        # 插入表格
        self.MyTable = QTableWidget(row, vol)
        self.MyTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        font = QtGui.QFont('微软雅黑', 10)


        # 设置字体、表头
        self.MyTable.horizontalHeader().setFont(font)
        self.MyTable.setHorizontalHeaderLabels(col_lst)

        # 设置竖直方向表头不可见
        self.MyTable.verticalHeader().setVisible(False)
        self.MyTable.setFrameShape(QFrame.NoFrame)

        # 构建表格插入数据
        for i in range(row):
            for j in range(vol):
                temp_data = data[i][j]  # 临时记录，不能直接插入表格
                data1 = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.MyTable.setItem(i, j, data1)

        connection.commit()
        cursor.close()

        cursor = connection.cursor()
        cursor.execute("SELECT title, reply_time, sender, receiver, blog_reply.text FROM blogs JOIN blog_reply ON (blog_time = update_time)")
        data1 = cursor.fetchall()
        col_lst = [tup[0] for tup in cursor.description]

        # 数据的大小
        row = len(data1)
        vol = len(data1[0])

        # 插入表格
        self.MyTable1 = QTableWidget(row, vol)
        font = QtGui.QFont('微软雅黑', 10)

        # 设置字体、表头
        self.MyTable1.horizontalHeader().setFont(font)
        self.MyTable1.setHorizontalHeaderLabels(col_lst)
        self.MyTable1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置竖直方向表头不可见
        self.MyTable1.verticalHeader().setVisible(False)
        self.MyTable1.setFrameShape(QFrame.NoFrame)

        for i in range(row):
            for j in range(vol):
                temp_data = data1[i][j]  # 临时记录，不能直接插入表格
                data10 = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.MyTable1.setItem(i, j, data10)

        # connection.close()

        self.titleqle = QLineEdit()
        self.textqle = QLineEdit()

        buttonBox = QDialogButtonBox()

        addButton = buttonBox.addButton("&添加博客", QDialogButtonBox.ActionRole)
        deleteButton = buttonBox.addButton("&删除博客", QDialogButtonBox.ActionRole)

        addButton.clicked.connect(partial(self.add_blog, cursor, connection, col_lst))
        deleteButton.clicked.connect(partial(self.delete_blog, cursor, connection))

        self.lb1 = QLabel("全部博客", self)
        self.lb1.setFont(font)
        self.lb2 = QLabel("全部评论", self)
        self.lb2.setFont(font)
        self.lb3 = QLabel("题目", self)
        self.lb4 = QLabel("内容", self)

        layout = QVBoxLayout()
        layout.addWidget(self.lb1)
        layout.addWidget(self.MyTable)
        layout.addWidget(self.lb3)
        layout.addWidget(self.titleqle)
        layout.addWidget(self.lb4)
        layout.addWidget(self.textqle)
        layout.addWidget(buttonBox)
        layout.addWidget(self.lb2)
        layout.addWidget(self.MyTable1)

        self.setLayout(layout)

    def add_blog(self, cursor, connection, col_lst):

        rowpos = self.MyTable.rowCount()
        self.MyTable.insertRow(rowpos)
        print(rowpos)
        title = self.titleqle.text()
        text = self.textqle.text()
        numcols = self.MyTable.columnCount()
        numrows = self.MyTable.rowCount()
        print(numcols)
        print(numrows)
        self.MyTable.setRowCount(numrows)
        self.MyTable.setColumnCount(numcols)

        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert = [title, self.username, text, time]
        print(insert)

        self.MyTable.setItem(rowpos, 0, QTableWidgetItem(title))
        self.MyTable.setItem(rowpos, 1, QTableWidgetItem(self.username))
        self.MyTable.setItem(rowpos, 2, QTableWidgetItem(text))
        self.MyTable.setItem(rowpos, 3, QTableWidgetItem(time))

        print("?")

        cursor.execute("INSERT INTO blogs VALUES (%s,%s,%s,%s)", (title, self.username, text, time))
        connection.commit()
        print("插入成功")

    def delete_blog(self, cursor, connection):
        reply = QMessageBox.question(self, 'Message', '确认删除该行?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 当前行
            row_2 = self.MyTable.currentRow()
            print(row_2)
            name = self.MyTable.item(row_2, 1).text()
            print(name)

            # 在数据库删除数据
            sql = "DELETE FROM blogs WHERE auther = '" + name + "'"
            print(sql)
            cursor.execute(sql)
            connection.commit()
            print("删除成功")

            # 删除表格
            self.MyTable.removeRow(row_2)


app = QApplication(sys.argv)
mp = MainPage("fnd@163.com")
mp.show()
sys.exit(app.exec_())
